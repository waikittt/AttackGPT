import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('ORIGINALITY_AI_API_KEY')         # Get API KEY from .env file
url = "https://api.originality.ai/api/v1/scan/ai"     # url of the end point of api

def get_updated_str(string, index, new_char):
    """
    Replace one of the characters within the string with another character
    """
    return string[:index] + new_char + string[index+1:]

def human_ai_detection(content:str):
  """
  Send the content to the originality.ai API to detect and interpret the result into
  different category depending on the score retrieved
  """

  payload = {"content": content}    # payload forming (content)
  headers = {                       # headers required for the ai scan
    'X-OAI-API-KEY': API_KEY,
    'Accept': 'application/json'
    }
  
  # Try except block to handle the condition where "content" argument is not of type string
  try:
    num_words = len(content.strip().split(" "))

    # Could not perform AI Detection if string length is less than 50
    if num_words >= 50:
      # Send content to endpoint for AI Scanning
      response = requests.request(method="POST", url=url, headers=headers, data=payload)
      response_status_code = response.status_code  # Retrieve the status code for the response

      if response_status_code == 422:
        # Handle Bad Request Error (422)
        raise Exception("Bad Request. Please try again.")
      
      elif response_status_code == 404:
        # Handle Not Found Error (404)
        raise Exception("Invalid API Endpoint. Please contact the development team")
      
      elif response_status_code == 429:
        # Handle Too Many Request Error (429)
        raise Exception("Rate Limit Exceeded. Please contact the development team.")
      
      elif response_status_code == 200:
        response_text = get_updated_str(response.text, 11, 'T')     
        res_obj = eval(response_text)                               # Convert string to dictionary object

        # Get the prediction result (ai and human)
        human_percentage = res_obj['score']['original'] * 100
        ai_percentage = res_obj['score']['ai'] * 100
        ai_prob = "Undetermined"

        # Probability of being AI generated (From MITRE.org)
        if ai_percentage <= 10:
          ai_prob = "Very unlikely"
        elif ai_percentage <= 40:
          ai_prob = "Unlikely"
        elif ai_percentage <= 60:
          ai_prob = "Unsure"
        elif ai_percentage <= 90:
          ai_prob = "Likely"
        elif ai_percentage <= 100:
          ai_prob = "Very likely"

        return {"human": human_percentage, "ai": ai_percentage, "ai_prob": ai_prob}
      
    else:
      return {"human": 0, "ai": 0, "ai_prob": "Undetermined"}
      
  except:
    raise Exception("Only string input can be accepted!")
  

if __name__ == "__main__":
  txt = "Apart from counting words and characters, our online editor can help you to improve word choice and writing style, and, optionally, help you to detect grammar mistakes and plagiarism. To check word count, simply place your cursor into the text box above and start typing, and that is all."
  res = human_ai_detection(txt)
  print(res)


  
  

# if __name__ == "__main__":
#   txt = "GPT, or Generative Pre-trained Transformer, is a type of artificial intelligence (AI) system designed to understand and generate human-like text. It's trained on a massive amount of data from the internet, which helps it learn patterns, grammar, and context. Once trained, GPT can generate coherent and contextually relevant text when given a prompt or question. Essentially, it's like having a smart language model that can understand and generate text based on the information it has learned."
#   res = human_ai_detection(txt)
#   print(res)

