import random

from django.core.management.base import BaseCommand

from apps.quiz.models import Answer, Question
from apps.rules.models import Rule


class Command(BaseCommand):
    help = "Generate study quiz questions from imported Highway Code rules."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Regenerate existing generated answers.")

    def handle(self, *args, **options):
        rules = list(Rule.objects.select_related("section").exclude(content=""))
        if len(rules) < 4:
            self.stdout.write(self.style.WARNING("Not enough rules to generate quiz questions."))
            return

        generated = 0
        for rule in rules:
            question_text = self.question_text(rule)
            question, created = Question.objects.get_or_create(
                rule=rule,
                question_text=question_text,
                defaults={
                    "category": "rules",
                    "difficulty": self.difficulty_for(rule),
                    "explanation": self.explanation(rule),
                    "is_active": True,
                },
            )
            if not created and not options["force"]:
                continue

            question.category = "rules"
            question.difficulty = self.difficulty_for(rule)
            question.explanation = self.explanation(rule)
            question.is_active = True
            question.save(update_fields=["category", "difficulty", "explanation", "is_active"])

            question.answers.all().delete()
            for text, is_correct in self.answers_for(rule, rules):
                Answer.objects.create(question=question, text=text, is_correct=is_correct)
            generated += 1

        self.stdout.write(self.style.SUCCESS(f"Generated or updated {generated} rule-based questions."))

    def question_text(self, rule):
        label = f"Rule {rule.rule_number}" if rule.rule_number else "this Highway Code page"
        title = rule.title or rule.section.title
        return f"{label}: which topic does this rule cover? {title}"

    def answers_for(self, rule, rules):
        correct = self.answer_label(rule)
        pool = [candidate for candidate in rules if candidate.pk != rule.pk]
        same_section = [candidate for candidate in pool if candidate.section_id == rule.section_id]
        distractors = random.sample(same_section, min(2, len(same_section)))
        remaining = [candidate for candidate in pool if candidate not in distractors]
        distractors += random.sample(remaining, min(3 - len(distractors), len(remaining)))
        answers = [(correct, True)] + [(self.answer_label(candidate), False) for candidate in distractors]
        random.shuffle(answers)
        return answers

    def answer_label(self, rule):
        number = f"Rule {rule.rule_number}" if rule.rule_number else "Highway Code guidance"
        return f"{number} - {rule.title or rule.section.title}"

    def explanation(self, rule):
        source = f" Source: {rule.source_url}" if rule.source_url else ""
        return f"Review {self.answer_label(rule)} in the official Highway Code.{source}"

    def difficulty_for(self, rule):
        if rule.section.rules.count() > 25:
            return "hard"
        if rule.section.rules.count() > 10:
            return "medium"
        return "easy"
