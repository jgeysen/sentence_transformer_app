"""Module for executing the prediction step."""
import logging
from typing import Any, List

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
        doc_id:

    Returns:
        List[dict[str, Any]]:
    """
    logger.info(f"Started inference for document {doc_id}.")

    sentences: List[dict[str, Any]] = load_sentences(doc_id=doc_id)
    page_mapping: dict[str, int] = load_page_mapping(doc_id=doc_id)
    model: SentenceTransformer = load_model()

    logger.info(
        f"Model and data successfully loaded for document {doc_id}. "
        f"Document {doc_id} contains {len(sentences)} sentences."
    )
    logger.info("Starting inference step now, this can take a while.")

    texts = [sentence["text"] for sentence in sentences]
    encodings = model.encode(
        sentences=texts,
        show_progress_bar=True,
        batch_size=10,
    )

    logger.info(f"Inference step for document {doc_id} successfully done.")

    for idx, sentence in enumerate(sentences):
        sentence["vector"] = encodings[idx]
        sentence["pages"] = [page_mapping[uuid] for uuid in sentence["pages"]]

    return sentences
