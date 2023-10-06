import requests


class STSModel():

	def __init__(self):
		self.API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
		self.headers = {"Authorization": "Bearer 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"}

	def query(self, payload):
		"""
		Make the request to the API endpoint to to get the similarity percentage
		"""

		response = requests.post(self.API_URL, headers=self.headers, json=payload)
		response.raise_for_status() # Raise an exception for 4xx and 5xx status codes
		return response.json()


	def payload_forming(self, source_sentence:str, target_sentence:str):
		"""
		Form the payload (input) that need to be passed into the query function
		"""
		return {
			"inputs": {
				"source_sentence": source_sentence,
				"sentences": [
					target_sentence
				]
			},
		}


	def similarity_checking(self, source_sentence, target_sentence):
		"""
		Compute the similarity percentage between the source sentence and the target sentence in % format (?/100)
		"""
		try: 
			payload = self.payload_forming(source_sentence, target_sentence)
			query_res = self.query(payload)
			similarity_percentage = round(query_res[0] * 100, 2)   # Between 0 and 1

			return similarity_percentage 
		
		except requests.exceptions.HTTPError as http_error:
			# Handle HTTP errors (e.g., 4xx or 5xx status codes)
			raise Exception(f"HTTP error occurred: {http_error}")

		except requests.exceptions.RequestException as request_error:
			# Handle other request-related exceptions (e.g., network errors)
			raise Exception(f"Request error occurred. Please try again.")



# if __name__ == "__main__":
# 	s1 = "A red apple is a fruit with a red or reddish skin. It's sweet, sometimes slightly tart, and widely enjoyed as a snack or ingredient in various dishes. Rich in nutrients and fiber, it comes in different varieties like Red Delicious, Fuji, Gala, and McIntosh, each with its own unique taste and texture."
# 	s2 = "A red apple is a fruit that is typically round with a red skin and a sweet or tart taste."
# 	model = STSModel()
# 	res = model.similarity_checking(s1, 123)
# 	print(res)


	
