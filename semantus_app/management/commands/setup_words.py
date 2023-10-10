from django.core.management.base import BaseCommand

from semantus_app.models import WordData


class Command(BaseCommand):
    help = "Initializes WordData with lemmatized words in German."

    def handle(self, *args, **kwargs):
        # check that WordData table is empty
        if not WordData.objects.exists():
            # load word embeddings

            # average embeddings that get lemmatized to the same word

            # iterate through lemmatized words and add them to WordData table
            for word in range(100):
                random_word = f"Word {word}"
                WordData.objects.create(word=random_word)
            self.stdout.write(
                self.style.SUCCESS("Successfully populated WordData table")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("WordData table is not empty, skipping population")
            )
