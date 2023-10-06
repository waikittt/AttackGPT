from textattack.transformations import CompositeTransformation
from textattack.constraints.pre_transformation import RepeatModification
from textattack.search_methods import GreedySearch
from textattack import Attack

from backend.chatgpt import ChatGPT
from backend.maximize_bias import MaximizeBias
from backend.gpt_model_wrapper import CustomGPTModelWrapper
from backend.word_add_gender import WordAddGender
from backend.word_add_race import WordAddRace
from backend.word_add_religion import WordAddReligion
from backend.word_add_sexuality import WordAddSexuality


def attack_recipe(target_bias):
    model = ChatGPT()
    model_wrapper = CustomGPTModelWrapper(model)
    goal_function = MaximizeBias(model_wrapper, target_bias=target_bias)

    transformation = CompositeTransformation(
        [
            WordAddGender(),
            WordAddSexuality(),
            WordAddRace(),
            WordAddReligion()
        ]
    )

    constraints = [RepeatModification()]

    search_method = GreedySearch()

    attack = Attack(goal_function, constraints, transformation, search_method)

    return attack




