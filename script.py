"""File containing the code to execute in the container."""
import pprint

from src.predict import predict

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    doc_id = "12345"
    x = predict(doc_id)
    pp.pprint(x)
