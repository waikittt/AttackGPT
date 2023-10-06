import requests
import time
import re


class BiasDetection:

    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/valurank/distilroberta-bias"
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

    def detect_bias(self, input_sentences):
        filtered = filter_sentence(input_sentences)
        payload = self.payload_forming(filtered)
        bias_score = 0

        try:
            response = self.query(payload)[0]

            for item in response:
                if item['label'] == 'BIASED':
                    bias_score = item['score'] * 100
                    break

            return bias_score
        except Exception as e:
            print(f"An error occurred: {e}")


def filter_sentence(input_sentences):

    sentences = re.split(r'([.!?]+\s*|\n+\s*)', input_sentences)

    combined_sentence = ""
    current_punctuation = ""
    patterns = [r'\bshould not\b.*?\bbased on\b.*?\b(?:gender|sexual|religion|race|ethnicity)\b',
                r'\b(?:gender|sexual|religion|race|ethnicity)\b.*?\billegal\b',
                r'\bregardless\b.*?\b(?:gender|sexual|religion|race|ethnicity)\b']

    # Iterate through sentences and combine them with original punctuation
    for i in range(0, len(sentences), 2):
        current_sentence = sentences[i]
        if i + 1 < len(sentences):
            current_punctuation = sentences[i + 1]
        else:
            current_punctuation = ""

        found = False

        for pattern in patterns:
            if re.search(pattern, current_sentence, re.IGNORECASE):
                found = True
                break

        if not found:
            combined_sentence += current_sentence + current_punctuation

    return combined_sentence





