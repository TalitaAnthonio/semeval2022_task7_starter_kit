"""A module for checking the format of the training dataset.

The requirements for the dataframe that contains the training data are:
* shall have the following columns:
    "Id", "Resolved pattern",
    "Article title", "Section header", "Previous context", "Sentence", "Follow-up context",
    "Filler1", "Filler2", "Filler3", "Filler4", "Filler5"
* the values in "Id" shall be integers
* the values in "Resolved pattern" shall be in the following set of options:
    "IMPLICIT REFERENCE", "ADDED COMPOUND", "METONYMIC REFERENCE", "FUSED HEAD"
* the values in "Sentence" shall have to contain a placeholder "______" for the insertion
* the fillers shall not be empty strings
* the ratings shall be floats in the range from 1 to 5
"""
import argparse
import logging

import pandas as pd

logging.basicConfig(level=logging.DEBUG)


def check_format_of_training_dataset(training_dataset: pd.DataFrame) -> None:
    """Check the format of dataframe with training data.

    :param training_dataset: dataframe with training set
    """
    logging.debug("Verifying the format of training dataset")

    required_columns = [
        "Id",
        "Resolved pattern",
        "Article title",
        "Section header",
        "Previous context",
        "Sentence",
        "Follow-up context",
        "Filler1",
        "Filler2",
        "Filler3",
        "Filler4",
        "Filler5",
    ]

    if not list(training_dataset.columns) == required_columns:
        raise ValueError(
            f"File does not have the required columns: {list(training_dataset.columns)} != {required_columns}."
        )

    for id in training_dataset["Id"]:
        try:
            int(id)
        except ValueError:
            raise ValueError(f"Id {id} is not a valid integer.")

    valid_patterns = [
        "IMPLICIT REFERENCE",
        "ADDED COMPOUND",
        "METONYMIC REFERENCE",
        "FUSED HEAD",
    ]

    for pattern in training_dataset["Resolved pattern"]:
        if pattern not in valid_patterns:
            raise ValueError(
                f"Resolved pattern {pattern} is not among {valid_patterns}."
            )

    for sentence in training_dataset["Sentence"]:
        if "______" not in sentence:
            raise ValueError(
                f"Sentence {sentence} does not contain placeholder '______'."
            )

    for filler_index in range(1, 6):
        for row_index, filler in enumerate(training_dataset[f"Filler{filler_index}"]):
            if not filler:
                raise ValueError(f"One of the fillers in row {row_index} is empty.")

    logging.debug(
        "Format checking for training dataset successful. No problems detected."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check format of file with training instances.")
    parser.add_argument(
        "--path_to_train",
        type=str,
        required=True,
        help="path to training instances",
    )
    args = parser.parse_args()
    training_dataset = pd.read_csv(args.path_to_train, delimiter="\t")
    check_format_of_training_dataset(training_dataset)
