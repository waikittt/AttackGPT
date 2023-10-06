import openai
import os
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:

    def __init__(self):
        self.API_KEY = os.getenv('CHATGPT_API_KEY')
        # API KEY for ChatGPT API
        openai.api_key = self.API_KEY

    def prompt_GPT(self, input_text):
        """
      Send the input text to GPT and retrieve the respective response

      Currently will be using "gpt-3.5-turbo" model which is the latest model for GPT-3.5.

      Feel free to change the model by subsituting it with one of the models provided in the below link
      https://platform.openai.com/docs/models/gpt-3-5
      """

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # GPT model that we are using (Can be modified)
                messages=[
                    {"role": "user", "content": input_text}
                ],
                max_tokens=300  # Maximum length of the reply (Can be modified)
            )

            # Retrieve the reply from ChatGPT
            # First element - indicate success retrievement of reply
            # Second element - the reply provided by ChatGPT
            reply = completion.choices[0].message['content']

            return reply

        except openai.error.APIError:
            # Handle API error here
            raise Exception(f"OpenAI API returned an API Error.")

        except openai.error.Timeout:
            # Handle request time out issue
            raise Exception(f"Request took too long to complete on OpenAI API.")

        except openai.error.RateLimitError:
            # Handle rate limit error
            raise Exception(f"OpenAI API request exceeded rate limit. Please contact the development team.")

        except openai.error.InvalidRequestError:
            # Handle API Connection error
            raise Exception(f"Invalid or malformed request provided (in this case might be non-string argument provided)")

        except openai.error.APIConnectionError:
            # Handle API Connection error
            raise Exception(f"Failed to connect to OpenAI API.")

        except openai.error.AuthenticationError:
            # Handle Authentication error
            raise Exception(f"API Key or token is invalid, expired or revoked. Please contact the development team.")

        except openai.error.ServiceUnavailableError:
            # Handle Server unavailable error
            raise Exception(f"OpenAI Servers temporarily unable.")


if __name__ == "__main__":
    msg = "what is medium class in the us"
    model = ChatGPT()
    resp = model.prompt_GPT(msg)
    print(resp)
