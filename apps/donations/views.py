from django.shortcuts import render

from .models import Charity


DEFAULT_CHARITIES = [
    {
        "name": "British Red Cross",
        "url": "https://www.redcross.org.uk/donate",
        "description": "Humanitarian aid across the UK and worldwide.",
        "icon": "cross",
    },
    {
        "name": "Road Safety Trust",
        "url": "https://roadsafetytrust.org.uk/",
        "description": "Improving road safety through research and education.",
        "icon": "shield",
    },
]


def donate(request):
    charities = list(Charity.objects.filter(is_active=True))
    return render(
        request,
        "donations/donate.html",
        {"charities": charities or DEFAULT_CHARITIES},
    )
