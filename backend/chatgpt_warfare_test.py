import unittest
from ai_detection_test import AIDetectionTest
from chatgpt_test import ChatgptTest
from sentence_similarity_test import SentenceSimilarityTest
from read_file_test import ReadFileTest
from word_add_gender_test import WordAddGenderTest
from word_add_sexuality_test import WordAddSexualityTest
from word_add_race_test import WordAddRaceTest
from word_add_religion_test import WordAddReligionTest

# Add other imports here if needed

def main():
    # Compile all the test suites into a list
    suiteList = []
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(AIDetectionTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(ChatgptTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(SentenceSimilarityTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(ReadFileTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(WordAddGenderTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(WordAddSexualityTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(WordAddRaceTest))
    suiteList.append(unittest.TestLoader().loadTestsFromTestCase(WordAddReligionTest))


    # combine all the test suites
    comboSuite = unittest.TestSuite(suiteList)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(comboSuite)

if __name__ == '__main__':
    main()