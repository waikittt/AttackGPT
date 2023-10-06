import unittest
from unittest.mock import Mock, patch
from ai_detection import human_ai_detection


class AIDetectionTest(unittest.TestCase):
    ############################### BLACK BOX TESTING ################################
    @patch("ai_detection.requests")
    def test_success_ai_detection(self, mock_requests):
        """
        This test tests whether the ai detection can properly process ai percentage <= 100
        """
        mock_response = Mock()
        mock_response.text = '{"success":true,"public_link":"https:\/\/app.originality.ai\/share\/b2lwsg7ruedtci0h","title":"API Scan","score":{"original":0.0009,"ai":0.9991}}'
        mock_response.status_code = 200
        mock_requests.request.return_value = mock_response

        txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is the end."
        result = human_ai_detection(txt)

        expected_res = {"human": 0.09, "ai": 99.91, "ai_prob": "Very likely"}
        
        _, kwargs = mock_requests.request.call_args_list[0]
        self.assertEqual(result, expected_res)
        self.assertEqual(kwargs['data'], {"content": txt})

    def test_fail_ai_detection_non_string(self):
        """
        This test tests whether the ai detection handle the error when non-string input is given
        """
        invalid_txt = 1234567

        with self.assertRaises(Exception) as context:
            human_ai_detection(invalid_txt)

        # Check if the expected error message is in the exception
        self.assertIn("Only string input can be accepted!", str(context.exception))

    @patch("ai_detection.requests")
    def test_fail_ai_detection_insufficient_length(self, mock_requests):
        """
        This test tests whether the ai detection handle the error when string input of length < 50 is given
        """
        mock_response = Mock()
        mock_requests.request.return_value = mock_response
        mock_response.status_code = 422

        invalid_txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is all."

        res = human_ai_detection(invalid_txt)
        self.assertEqual(res, {"human": 0, "ai": 0, "ai_prob": "Undetermined"})
        

    ############################### WHITE BOX TESTING ################################
    # @patch("ai_detection.requests")
    # def test_success_likely_ai_detection(self, mock_requests):
    #     """
    #     This test tests whether the ai detection can properly process ai percentage <= 90
    #     """
    #     mock_response = Mock()
    #     mock_response.status_code = 200
    #     mock_response.text = '{"success":true,"public_link":"https:\/\/app.originality.ai\/share\/b2lwsg7ruedtci0h","title":"API Scan","score":{"original":0.13,"ai":0.87}}'
    #     mock_requests.request.return_value = mock_response

    #     txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is the end."
    #     result = human_ai_detection(txt)

    #     expected_res = {"human": 13, "ai": 87, "ai_prob": "Likely"}
        
    #     _, kwargs = mock_requests.request.call_args_list[0]
    #     self.assertEqual(result, expected_res)
    #     self.assertEqual(kwargs['data'], {"content": txt})

    # @patch("ai_detection.requests")
    # def test_success_unsure_ai_detection(self, mock_requests):
    #     """
    #     This test tests whether the ai detection can properly process ai percentage <= 60
    #     """
    #     mock_response = Mock()
    #     mock_response.text = '{"success":true,"public_link":"https:\/\/app.originality.ai\/share\/b2lwsg7ruedtci0h","title":"API Scan","score":{"original":0.4285,"ai":0.5715}}'
    #     mock_response.status_code = 200
    #     mock_requests.request.return_value = mock_response

    #     txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is the end."
    #     result = human_ai_detection(txt)

    #     expected_res = {"human": 42.85, "ai": 57.15, "ai_prob": "Unsure"}
        
    #     args, kwargs = mock_requests.request.call_args_list[0]
    #     self.assertEqual(result, expected_res)
    #     self.assertEqual(kwargs['data'], {"content": txt})

    # @patch("ai_detection.requests")
    # def test_success_unlikely_ai_detection(self, mock_requests):
    #     """
    #     This test tests whether the ai detection can properly process ai percentage <= 40
    #     """
    #     mock_response = Mock()
    #     mock_response.text = '{"success":true,"public_link":"https:\/\/app.originality.ai\/share\/b2lwsg7ruedtci0h","title":"API Scan","score":{"original": 0.60,"ai":0.40}}'
    #     mock_response.status_code = 200
    #     mock_requests.request.return_value = mock_response

    #     txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is the end."
    #     result = human_ai_detection(txt)

    #     expected_res = {"human": 60, "ai": 40, "ai_prob": "Unlikely"}
        
    #     args, kwargs = mock_requests.request.call_args_list[0]
    #     self.assertEqual(result, expected_res)
    #     self.assertEqual(kwargs['data'], {"content": txt})

    # @patch("ai_detection.requests")
    # def test_success_very_unlikely_ai_detection(self, mock_requests):
    #     """
    #     This test tests whether the ai detection can properly process ai percentage <= 10
    #     """
    #     mock_response = Mock()
    #     mock_response.text = '{"success":true,"public_link":"https:\/\/app.originality.ai\/share\/b2lwsg7ruedtci0h","title":"API Scan","score":{"original":0.958,"ai":0.042}}'
    #     mock_response.status_code = 200
    #     mock_requests.request.return_value = mock_response

    #     txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is the end."
    #     result = human_ai_detection(txt)

    #     expected_res = {"human": 95.80, "ai": 4.20, "ai_prob": "Very unlikely"}
        
    #     args, kwargs = mock_requests.request.call_args_list[0]
    #     self.assertEqual(result, expected_res)
    #     self.assertEqual(kwargs['data'], {"content": txt})
