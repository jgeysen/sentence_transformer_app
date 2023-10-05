"""Module for executing the prediction step."""
from typing import Any, List

from sentence_transformers import SentenceTransformer

from src.data_loader import load_model, load_page_mapping, load_sentences


def predict(doc_id: str) -> List[dict[str, Any]]:
    """
    Perform prediction on the given doc_id.

    Arguments:
        doc_id:

    Returns:
        List[dict[str, Any]]:
    """
    sentences: List[dict[str, Any]] = load_sentences(doc_id=doc_id)
    page_mapping: dict[str, int] = load_page_mapping(doc_id=doc_id)
    model: SentenceTransformer = load_model()

    sentences = sentences[:10]  # there's 3519 sentences in the original dataset
    texts = [sentence["text"] for sentence in sentences]
    encodings = model.encode(
        sentences=texts,
        show_progress_bar=True,
        batch_size=10,
    )

    result = [None] * len(sentences)
    for idx, sentence in enumerate(sentences):
        text = sentence["text"]
        pages_uuid = sentence["pages"]
        pages_int = [page_mapping[uuid] for uuid in pages_uuid]
        encoding = encodings[idx]
        result[idx] = {"text": text, "vector": encoding.shape, "pages": pages_int}
    return result


if __name__ == "__main__":
    doc_id = "12345"
    x = predict(doc_id)
    print(x)
