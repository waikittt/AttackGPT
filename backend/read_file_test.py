from read_file import read_prompts_from_file
import os
import unittest

class ReadFileTest(unittest.TestCase):
    def test_valid_file(self):
        """
        This test tests whether the content of the file can be properly read in the expected manner
        """
        # Create a temporary file with valid content
        with open('valid_file.txt', 'w', encoding='utf-8') as f:
            f.write("Prompt 1\nPrompt 2\nPrompt 3")

        prompts = read_prompts_from_file('valid_file.txt')

        # Verify that the function returns the expected list of prompts
        self.assertEqual(prompts, ["Prompt 1", "Prompt 2", "Prompt 3"])

        # Clean up the temporary file
        os.remove('valid_file.txt')

    def test_non_existent_file(self):
        """
        This test tests whether the error can be handled properly when the file that supposed to read does not exist
        """
        # Test with a non-existent file, which should raise FileNotFoundError
        with self.assertRaises(Exception) as context:
            read_prompts_from_file('non_existent_file.txt')

        # Check that the exception message mentions the non-existent file
        self.assertIn("non_existent_file.txt does not exist", str(context.exception))
