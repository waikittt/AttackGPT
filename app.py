from flask import Flask, render_template, request
from backend.sentence_similarity import STSModel
from backend.chatgpt import ChatGPT
from backend.ai_detection import human_ai_detection
from backend.main import bias_attack
from backend.read_file import read_prompts_from_file

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download' , methods=['POST'])
def download():
        
    if request.method == 'POST':
        url = request.form['url']
        print(url)

    if not url:
        return 'Invalid URL. Please provide a valid URL.'
    
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the entire HTML content to a file
            with open('downloaded_results.html', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

            return render_template('downloaded.html')
        else:
            return f'Failed to download webpage. Status code: {response.status_code}'
        
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/results', methods=['GET', 'POST'])
def results():    
    """    
    Results for Bias attack.
    """
    chatgpt = ChatGPT()    

    # Original Text
    try:
        input_text = request.args.get('oriInput')
        output_text = chatgpt.prompt_GPT(input_text)   
            
        attack_results = bias_attack(input_text, output_text)
        oriText = attack_results[0]
        oriAnswer = attack_results[1]
        oriScore = f"{attack_results[2]:.2f}"
        oriSentiment = attack_results[3]

        # Perturbed Text
        perturbText = attack_results[4]
        perturbAnswer = attack_results[5]
        perturbScore = f"{attack_results[6]:.2f}"
        perturbSentiment = attack_results[7]

        # If the original text and the perturbed text are the same, the attack failed
        if input_text == perturbText:
            return render_template('attack_failed.html')  

        # Similarity
        sts_model = STSModel()
        similarity = sts_model.similarity_checking(oriAnswer, perturbAnswer)

    except Exception as e:
          return render_template('error.html', errorMessage = str(e))
    
    else:    
        ori_percentage = human_ai_detection(oriAnswer) 
        ori_human_percentage = f"{ori_percentage['human']:.2f}"
        ori_ai_percentage = f"{ori_percentage['ai']:.2f}"
        oriPossible = ori_percentage['ai_prob']

        pt_percentage = human_ai_detection(perturbAnswer)
        pt_human_percentage = f"{pt_percentage['human']:.2f}"
        pt_ai_percentage = f"{pt_percentage['ai']:.2f}"
        perturbPossible = pt_percentage['ai_prob']

        short = ""
        if oriPossible == "Undetermined" or perturbPossible == "Undetermined":
            short = "The generated answers are too short to be detected. (Both need at least 50 words)"

        return render_template('results.html', similarity=similarity, oriText = oriText, oriAnswer = oriAnswer, perturbText = perturbText, \
                            perturbAnswer = perturbAnswer, oriPossible = oriPossible, perturbPossible = perturbPossible, \
                                oriProgress = ori_ai_percentage, oriProgress2 = ori_human_percentage, oriProgress3 = oriScore, oriSentiment = oriSentiment,  \
                                    perturbProgress = pt_ai_percentage, perturbProgress2 = pt_human_percentage, \
                                        perturbProgress3 = perturbScore, perturbSentiment = perturbSentiment, answerShort = short)



@app.route('/results2', methods=['GET', 'POST'])
def results2():
    """
    Results for TextAttack attack.
    """
    prompt_num = int(request.args.get('prompt'))
    attack_code = request.args.get('attack')

    try: 
        oriText = read_prompts_from_file('attack_results/original_prompts.txt')[prompt_num]
        perturbText = ""    

        # Get the perturbed text based on the attack recipe
        if attack_code == 'dwb':
            perturbText = read_prompts_from_file('attack_results/dwb_attack.txt')[prompt_num]
        elif attack_code == 'tb':
            perturbText = read_prompts_from_file('attack_results/tb_attack.txt')[prompt_num]
        elif attack_code == 'tf':
            perturbText = read_prompts_from_file('attack_results/tf_attack.txt')[prompt_num]
        elif attack_code == 'cl':
            perturbText = read_prompts_from_file('attack_results/cl_attack.txt')[prompt_num]

        # Generate answers for both original and perturbed text
        chatgpt = ChatGPT()
        oriAnswer = chatgpt.prompt_GPT(oriText)             
        perturbAnswer = chatgpt.prompt_GPT(perturbText)
        
        # Similarity
        sts_model = STSModel()
        similarity = sts_model.similarity_checking(oriAnswer, perturbAnswer)

    except Exception as e:
        return render_template('error.html', errorMessage = str(e))

    else:
        ori_percentage = human_ai_detection(oriAnswer) 
        ori_human_percentage = f"{ori_percentage['human']:.2f}"
        ori_ai_percentage = f"{ori_percentage['ai']:.2f}"
        oriPossible = ori_percentage['ai_prob']

        pt_percentage = human_ai_detection(perturbAnswer)
        pt_human_percentage = f"{pt_percentage['human']:.2f}"
        pt_ai_percentage = f"{pt_percentage['ai']:.2f}"
        perturbPossible = pt_percentage['ai_prob']

        short = ""
        if oriPossible == "Undetermined" or perturbPossible == "Undetermined":
            short = "The generated answers are too short to be detected. (Both need at least 50 words)"

        return render_template('results2.html', similarity=similarity, oriText = oriText, oriAnswer = oriAnswer, perturbText = perturbText, \
                            perturbAnswer = perturbAnswer, oriPossible = oriPossible, perturbPossible = perturbPossible, \
                             oriProgress = ori_ai_percentage, oriProgress2 = ori_human_percentage,  \
                                  perturbProgress = pt_ai_percentage, perturbProgress2 = pt_human_percentage, answerShort = short)


if __name__ == '__main__':    
    app.run()

    