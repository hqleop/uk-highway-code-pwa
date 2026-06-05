import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from apps.rules.models import Rule, RuleSection


INDEX_URL = "https://www.gov.uk/guidance/the-highway-code"


class Command(BaseCommand):
    help = "Import Highway Code sections and rules from the official gov.uk guidance."

    def add_arguments(self, parser):
        parser.add_argument("--limit-sections", type=int, default=0)
        parser.add_argument("--flush", action="store_true")

    def handle(self, *args, **options):
        if options["flush"]:
            Rule.objects.all().delete()
            RuleSection.objects.all().delete()

        soup = self.fetch(INDEX_URL)
        links = self.section_links(soup)
        if options["limit_sections"]:
            links = links[: options["limit_sections"]]

        for order, (title, url) in enumerate(links, start=1):
            section, _ = RuleSection.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "order": order,
                    "icon": self.icon_for(title),
                    "source_url": url,
                },
            )
            self.stdout.write(f"Importing {title}")
            self.import_section(section, url)

        self.stdout.write(self.style.SUCCESS("Highway Code import completed."))

    def fetch(self, url):
        response = requests.get(url, timeout=30, headers={"User-Agent": "HighwayCodeStudyPWA/1.0"})
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def section_links(self, soup):
        links = []
        ignored_titles = {"see all updates", "print this page"}
        for anchor in soup.select("a[href*='/guidance/the-highway-code/']"):
            title = " ".join(anchor.get_text(" ", strip=True).split())
            href = anchor.get("href")
            if not title or not href:
                continue
            if title.lower() in ignored_titles:
                continue
            url = urljoin(INDEX_URL, href)
            if url == INDEX_URL or (title, url) in links:
                continue
            if "#" in url:
                continue
            links.append((title, url))
        return links

    def import_section(self, section, url):
        soup = self.fetch(url)
        content_root = soup.select_one(".govspeak") or soup.select_one("main") or soup
        current_number = ""
        current_title = ""
        chunks = []
        created = 0

        for node in content_root.find_all(["h2", "h3", "p", "ul", "ol"], recursive=True):
            text = " ".join(node.get_text(" ", strip=True).split())
            if not text:
                continue
            match = re.match(r"^Rule\s+([0-9A-Za-z]+)\b[:.\s-]*(.*)$", text)
            if match:
                if chunks:
                    self.save_rule(section, current_number, current_title, chunks, url)
                    created += 1
                current_number = match.group(1)
                current_title = match.group(2)[:255]
                chunks = []
                continue
            if current_number:
                chunks.append(str(node))

        if chunks:
            self.save_rule(section, current_number, current_title, chunks, url)
            created += 1

        if created == 0:
            self.save_rule(section, "", section.title, [str(content_root)], url)

    def save_rule(self, section, number, title, chunks, url):
        Rule.objects.update_or_create(
            section=section,
            rule_number=number,
            defaults={
                "title": title,
                "content": "\n".join(chunks),
                "source_url": url,
                "has_image": "img" in "".join(chunks).lower(),
            },
        )

    def icon_for(self, title):
        title = title.lower()
        if "pedestrian" in title:
            return "person-standing"
        if "cyclist" in title:
            return "bike"
        if "motorcycl" in title:
            return "bike"
        if "motorway" in title:
            return "route"
        if "sign" in title:
            return "triangle-alert"
        return "book-open"
