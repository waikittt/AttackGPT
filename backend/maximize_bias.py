from textattack.goal_functions.text import TextToTextGoalFunction
from backend.bias_detection import BiasDetection


class MaximizeBias(TextToTextGoalFunction):

    def __init__(self, *args, target_bias=0.0, **kwargs):
        self.target_bias = target_bias
        super().__init__(*args, **kwargs)

    def _is_goal_complete(self, model_output, _):
        bias_score = self._get_score(model_output, _)
        return bias_score >= self.target_bias

    def _get_score(self, model_output, _):
        bias_score = get_score(model_output)
        return bias_score


def get_score(a):
    model = BiasDetection()
    score = model.detect_bias(a)
    return score
