from textattack.goal_functions.text import TextToTextGoalFunction

from backend.sentence_similarity import STSModel


class MinimizeSimilarity(TextToTextGoalFunction):

    def __init__(self, *args, target_similarity=0.0, **kwargs):
        self.target_similarity = target_similarity
        super().__init__(*args, **kwargs)

    def _is_goal_complete(self, model_output, _):
        similarity_score = self._get_score(model_output, _)
        return similarity_score <= self.target_similarity

    def _get_score(self, model_output, _):
        similarity_score = get_score(model_output, self.ground_truth_output)
        return similarity_score


def get_score(a, b):

    model = STSModel()
    score = model.similarity_checking(a, b)
    return score
