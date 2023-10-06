import unittest
from unittest.mock import Mock, patch
from sentence_similarity import STSModel
import requests


class SentenceSimilarityTest(unittest.TestCase):
    @patch('sentence_similarity.requests')
    def test_success_check_similarity(self, mock_requests):
        """
        This test tests whether the sentence similarity can be checked and retrieved properly
        """
        sts = STSModel()
        mock_respone = Mock()       # mock respone object
        mock_respone.json.return_value = [0.725885744334234]
        mock_requests.post.return_value = mock_respone

        source_sent = "The apple has already rotten"
        target_sent = "The apple was spoiled"
        similarity_percent_res = sts.similarity_checking(source_sent, target_sent)

        # check whether the similarity percentage can be retrieved and in correct format
        self.assertEqual(similarity_percent_res, 72.59) 

    @patch('sentence_similarity.requests.post')
    def test_fail_check_similarity_one_invalid(self, mock_post):
        """
        This test tests whether the similarity checking can handle the error when one of the argument is not of type string (invalid).
        """
        sts = STSModel()
        error_message = "400 Client Error: Bad Request"
        mock_http_error = requests.exceptions.HTTPError(error_message)

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = mock_http_error
        mock_post.return_value = mock_response

        source_sent = 1234
        target_sent = "The apple was spoiled"

        with self.assertRaises(Exception) as context:
            sts.similarity_checking(source_sent, target_sent)

        self.assertEqual(mock_post.call_count, 1)
        self.assertIn(f"HTTP error occurred: 400 Client Error: Bad Request", str(context.exception))

    @patch('sentence_similarity.requests.post')
    def test_fail_check_similarity_both_invalid(self, mock_post):
        """
        This test tests whether the similarity checking can handle the error when both arguments are not of type string (invalid).
        """
        sts = STSModel()
        error_message = "400 Client Error: Bad Request"
        mock_http_error = requests.exceptions.HTTPError(error_message)

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = mock_http_error
        mock_post.return_value = mock_response

        source_sent = 1234
        target_sent = 1234

        with self.assertRaises(Exception) as context:
            sts.similarity_checking(source_sent, target_sent)

        self.assertEqual(mock_post.call_count, 1)
        self.assertIn(f"HTTP error occurred: 400 Client Error: Bad Request", str(context.exception))


