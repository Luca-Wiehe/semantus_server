import os
from collections import defaultdict
from django.core.management.base import BaseCommand

from semantus_app.models import WordData
import spacy
import numpy as np


class Command(BaseCommand):
    help = "Initializes WordData with lemmatized words in German."

    def handle(self, *args, **kwargs):
        # load spacy model
        nlp = spacy.load("de_core_news_sm")

        def lemmatize_german_word(word_to_lemmatize):
            """
            Lemmatizes a word in German (i.e. returns the base form of the word)

            Parameters:
                word_to_lemmatize: word to lemmatize

            Returns:
                lemma: base form of the word
            """
            return nlp(word_to_lemmatize)[0].lemma_

        # check that WordData table is empty
        if not WordData.objects.exists():
            # path to embeddings file (relative to current location)
            file_path = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    )
                ),
                "embeddings",
                "german-embeddings.txt",
            )

            # dictionary of all words
            all_words = defaultdict(list)

            # load embeddings file
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # remove line breaks
                    line = line.replace("\n", "")

                    # get all components
                    components = line.split(" ")

                    # decode word and obtain lemma
                    word = (
                        components[0][2:-1].encode("latin-1").decode("unicode-escape")
                    )
                    word = word.encode("latin1").decode("utf-8")

                    lemma = lemmatize_german_word(word)

                    # append lemma and vector to all_words
                    all_words[lemma].append(
                        [float(component) for component in components[1:-1]]
                    )

            # iterate through lemmatized words and add them to WordData table
            for word, vectors in all_words.items():
                if len(vectors) > 1:
                    # average embeddings that get lemmatized to the same word
                    np_vectors = np.array(vectors)
                    average_vector = np.mean(np_vectors, axis=0)

                    # convert np-array to list and create entry in WordData table
                    WordData.objects.create(
                        word=word,
                        vector=" ".join(
                            map(lambda x: str(round(x, 6)), average_vector.tolist())
                        ),
                    )
                else:
                    # create entry in WordData table
                    WordData.objects.create(
                        word=word, vector=" ".join(map(str, vectors[0]))
                    )

            self.stdout.write(
                self.style.SUCCESS("Successfully populated WordData table")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "WordData table is not empty, skipping population. Delete db.sqlite3 to repopulate."
                )
            )
