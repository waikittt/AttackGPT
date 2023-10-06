from datasets import load_dataset
from textattack.datasets import HuggingFaceDataset
from data import PEOPLE, PERSONAL_PRONOUNS


def transforms(examples):
    examples["chatgpt_answers"] = examples["chatgpt_answers"][0]
    return examples


def dataset_load():

    dataset_dict = load_dataset("Hello-SimpleAI/HC3", name="finance")

    train_dataset = dataset_dict["train"]
    train_dataset = train_dataset.filter(
        lambda x: any((" " + word.lower() + " ") in x["question"].lower() for word in PEOPLE) or any(
            (" " + pronoun.lower() + " ") in x["question"].lower() for pronoun in PERSONAL_PRONOUNS))

    train_dataset.set_transform(transforms)

    input_columns = ["question"]
    output_column = "chatgpt_answers"

    dataset = HuggingFaceDataset(train_dataset, dataset_columns=(input_columns, output_column))

    return dataset

