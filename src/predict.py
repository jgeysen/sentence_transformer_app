"""Module for executing the prediction step."""
import logging
from typing import Any, List

import torch
from sentence_transformers import SentenceTransformer

from src.data_loader import load_model, load_page_mapping, load_sentences

# create logger
logger = logging.getLogger("inference_step")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def predict(doc_id: str) -> List[dict[str, Any]]:
    """
    Perform prediction on the given doc_id.

    Arguments:
        doc_id: id of the document.

    Returns:
        List[dict[str, Any]]: a list of dictionaries, holding the text, the
        torch vector and the pages for each sentence.
    """
    logger.info(f"Started inference for document {doc_id}.")

    sentence_data: List[dict[str, Any]] = load_sentences(doc_id=doc_id)
    page_mapping: dict[str, int] = load_page_mapping(doc_id=doc_id)
    model: SentenceTransformer = load_model()

    logger.info(
        f"Model and data successfully loaded for document {doc_id}. "
        f"Document {doc_id} contains {len(sentence_data)} sentences."
    )

    if torch.cuda.is_available():
        model.to("cuda")
        logger.info("Using GPU for inference.")
    else:
        logger.info(
            "There is no GPU available on your instance/container. "
            "Continuing with CPU. Inference step might be slow."
        )

    logger.info("Starting inference step.")

    sentences: List[str] = [sentence["text"] for sentence in sentence_data]
    encodings = model.encode(
        sentences=sentences,
        show_progress_bar=True,
    )

    logger.info(f"Inference step for document {doc_id} successfully done.")

    for idx, sentence in enumerate(sentence_data):
        sentence["vector"] = encodings[idx]
        sentence["pages"] = [page_mapping[uuid] for uuid in sentence["pages"]]

    return sentence_data
