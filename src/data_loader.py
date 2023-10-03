"""Module holding methods to load data and models."""
import csv
import json
from typing import List

from sentence_transformers import SentenceTransformer

from src.settings import Settings


def load_sentences(
    doc_id: str, settings: Settings = Settings()
) -> List[dict[str, str]]:
    """
    Load sentence data from the data folder.

    Arguments:
            doc_id: id of the document. There should be a file called
            `texts_{doc_id}.json` in the DATA_LOCATION folder.
            settings: Settings object which holds o.a. the location of the data to load.

    Returns:
            List[dict[str, str]]: Returns a list of dictionaries, where each sentence
            is represented as a dict with keys "text", which is a string, and "pages",
            which is a list of UUID's.
    """
    text_location = settings.DATA_LOCATION
    with open(f"{text_location}/texts_{doc_id}.json", "r") as file:
        data = json.load(file)
    return data


def load_page_mapping(doc_id: str, settings: Settings = Settings()) -> dict[str, int]:
    """
    Load the mapping between page references and page numbers.

    Arguments:
            doc_id: id of the document. There should be a file called
            `pages_{doc_id}.csv` in the DATA_LOCATION folder.
            settings: Settings object which holds o.a. the location of the data to load.

    Returns:
            dict: A dictionary containing a mapping between UUID's, representing
            references to pages and integers, representing the actual page number.
    """
    data_location = settings.DATA_LOCATION
    with open(f"{data_location}/pages_{doc_id}.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip the headers
        data = {row[0]: int(row[1]) for row in reader if len(row) == 2}
    return data


def load_model(settings: Settings = Settings()) -> SentenceTransformer:
    """
    Load the model.

    Returns:
            SentenceTransformer: sentence transformer model.
    """
    data_location = settings.DATA_LOCATION
    model_name = settings.MODEL_NAME
    return SentenceTransformer(f"{data_location}/models/{model_name}")
