import unittest
from word_add_race import WordAddRace
from textattack.shared.attacked_text import AttackedText
from data import RACE

class WordAddRaceTest(unittest.TestCase):
    def test_success_gender_word_swap_personal_pronouncs(self):
        """
        Test whether the race word swap transformation work as expected when there exisit PERSONAL_PRONOUNCS term in the sentence
        """
        test_obj = WordAddRace()
        test_txt = AttackedText('Can I know what is the possible chance to get loan?')
        test_idx = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

        expected_results = []
        for race in RACE:
            modified_str = AttackedText(f'Can I, as a {race}, know what is the possible chance to get loan?').words
            expected_results.append(modified_str)

        res = test_obj._get_transformations(test_txt, test_idx)
        self.assertTrue(all(attacked_txt.words in expected_results for attacked_txt in res))   # Check whether all transformed text is one of the expected results

    def test_success_race_word_swap_people(self):
        """
        Test whether the race word swap transformation work as expected when there exisit PEOPLE term in the sentence
        """
        test_obj = WordAddRace()
        test_txt = AttackedText('What is the possible chance for human to get loan?')
        test_idx = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

        expected_results = []
        for race in RACE:
            modified_str = AttackedText(f'What is the possible chance for {race} human to get loan?').words
            expected_results.append(modified_str)

        res = test_obj._get_transformations(test_txt, test_idx)
        self.assertTrue(all(attacked_txt.words in expected_results for attacked_txt in res))   # Check whether all transformed text is one of the expected results

    def test_fail_race_word_swap(self):
        """
        Test whether the race word swap transformation able to detect the error when non-AttackText object being passed
        """
        test_obj = WordAddRace()
        test_txt = "Hello, this is a wrong text!"
        test_idx = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

        with self.assertRaises(AttributeError):
            test_obj._get_transformations(test_txt, test_idx)


# if __name__ == "__main__":
#     unittest.main()