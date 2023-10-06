import requests
import time


class SentimentAnalysis:

    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.headers = {"Authorization": "Bearer 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"}

    def payload_forming(self, sentence):
        payload = {
            "inputs": sentence
        }
        return payload

    def query(self, payload):

        while True:
            try:
                response = requests.post(self.API_URL, headers=self.headers, json=payload)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                # Handle the error as needed, e.g., log it or raise a custom exception
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                # Handle the error as needed, e.g., log it or raise a custom exception
            except Exception as err:
                print(f"An unexpected error occurred: {err}")

            print("Retrying in 5 seconds...")
            time.sleep(5)

    def sentiment_analysis(self, input_sentence):
        payload = self.payload_forming(input_sentence)

        try:
            response = self.query(payload)[0]
            return response
        except Exception as e:
            print(f"An error occurred: {e}")

    def sentiment(self, input_sentence):
        sentiment_score = self.sentiment_analysis(input_sentence)
        res = sentiment_score[0]['label']

        return res.capitalize()
