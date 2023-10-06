import unittest
from unittest.mock import Mock, patch
import openai

from chatgpt import ChatGPT

class ChatgptTest(unittest.TestCase):
    @patch('chatgpt.openai')
    def test_success_chatgpt_generation(self, mock_openai):
        """
        This test tests whether the input and output can be sent and retrieved correctly.
        """
        chatgpt = ChatGPT()
        mock_content = "What do you think about the unit FIT3162 in Monash University?"
        expected_output = "I think it is pretty interesting."

        mock_completion = Mock()        # Create a mock object
        mock_choices = Mock()           # Create a mock object
        mock_choices.message = {'content': expected_output}
        mock_completion.choices = [mock_choices]
        mock_openai.ChatCompletion.create.return_value = mock_completion        # Defined the return value
        
        res = chatgpt.prompt_GPT(mock_content)      # Call the function

        # Validate whether the output of the function as expected
        _, kwargs = mock_openai.ChatCompletion.create.call_args_list[0]
        self.assertEqual(kwargs['messages'],[{"role": "user", "content": mock_content}])
        self.assertEqual(res, expected_output)

    @patch('openai.ChatCompletion.create', side_effect=openai.error.InvalidRequestError('Test error message', param='param_value'))
    def test_fail_chatgpt_generation(self, mock_openai_create):
        """
        This test tests whether error from invalid input can be handled properly.
        """
        chatgpt = ChatGPT()

        # Call the function with a mock that raises an APIError
        with self.assertRaises(Exception) as context:
            chatgpt.prompt_GPT(1234567)
        
        # Check if the expected error message is in the exception
        self.assertIn(f"Invalid or malformed request provided (in this case might be non-string argument provided)", str(context.exception))

