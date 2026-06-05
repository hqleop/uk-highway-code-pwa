from django.core.management.base import BaseCommand

from apps.quiz.models import Answer, Question


SAMPLES = [
    {
        "category": "rules",
        "difficulty": "easy",
        "question_text": "Where should you look for the official legal guidance used by this app?",
        "explanation": "The app stores source links and imports learning content from the official gov.uk Highway Code.",
        "answers": [
            ("The official Highway Code on gov.uk", True),
            ("A social media driving group", False),
            ("A private blog with road tips", False),
            ("An old printed leaflet with no date", False),
        ],
    },
    {
        "category": "signs",
        "difficulty": "easy",
        "question_text": "What is the main purpose of road signs in Highway Code study?",
        "explanation": "Road signs communicate mandatory instructions, warnings, directions, and road information.",
        "answers": [
            ("To give instructions, warnings, directions, and information", True),
            ("To decorate roads", False),
            ("To replace all driver judgement", False),
            ("To apply only to learner drivers", False),
        ],
    },
    {
        "category": "theory",
        "difficulty": "medium",
        "question_text": "What should you do when a rule page in this app links to gov.uk?",
        "explanation": "The source link is included for attribution and for checking the latest official text.",
        "answers": [
            ("Use it to verify the official source and latest wording", True),
            ("Ignore it because the app has no source requirements", False),
            ("Treat it as advertising", False),
            ("Use it only after passing a test", False),
        ],
    },
]


class Command(BaseCommand):
    help = "Create starter quiz questions for a fresh local database."

    def handle(self, *args, **options):
        for item in SAMPLES:
            question, _ = Question.objects.update_or_create(
                question_text=item["question_text"],
                defaults={
                    "category": item["category"],
                    "difficulty": item["difficulty"],
                    "explanation": item["explanation"],
                    "is_active": True,
                },
            )
            question.answers.all().delete()
            for text, is_correct in item["answers"]:
                Answer.objects.create(question=question, text=text, is_correct=is_correct)
        self.stdout.write(self.style.SUCCESS("Starter quiz questions created."))
