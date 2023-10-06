from textattack.models.wrappers import ModelWrapper


class CustomGPTModelWrapper(ModelWrapper):

    def __init__(self, model):
        self.model = model

    def __call__(self, text_input_list):
        responses = []

        for input_text in text_input_list:
            response = self.model.prompt_GPT(input_text)
            responses.append(response)

        return responses
