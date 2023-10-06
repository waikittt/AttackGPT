import numpy as np
from textattack.transformations import WordSwap
from backend.data import PEOPLE, PERSONAL_PRONOUNS, SEXUALITY


class WordAddSexuality(WordSwap):

    def __init__(self, n=2, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    def _get_replacement_words(self, word):
        return np.random.choice(SEXUALITY, self.n)

    def _get_transformations(self, current_text, indices_to_modify):
        words = current_text.words
        transformed_texts = []
        last = list(indices_to_modify)[-1]

        for i in indices_to_modify:
            word_to_replace = words[i]

            if word_to_replace.capitalize() in PEOPLE or word_to_replace.capitalize() in PERSONAL_PRONOUNS:

                if i != 0 and (words[i - 1].capitalize() in PEOPLE or words[i - 1].capitalize() in PERSONAL_PRONOUNS):
                    continue

                replacement_words = self._get_replacement_words(word_to_replace)
                transformed_texts_idx = []

                for r in replacement_words:
                    if word_to_replace.capitalize() in PEOPLE:
                        r = r + " " + word_to_replace
                    elif word_to_replace.capitalize() in PERSONAL_PRONOUNS:
                        r = word_to_replace + ", as a " + r + ","

                    transformed_texts_idx.append(current_text.replace_word_at_index(i, r))

                transformed_texts.extend(transformed_texts_idx)

        return transformed_texts


# if __name__ == "__main__":
#     from textattack.augmentation import Augmenter
#     transformation = WordAddSexuality()
#     augmenter = Augmenter(transformation=transformation)
#     s = 'What is the possible chance for human to get loan?'
#     print(augmenter.augment(s))