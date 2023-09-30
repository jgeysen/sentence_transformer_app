from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim, isclose
from torch import tensor

# my notebook is running 3.9.17 with sentence-transformers 2.2.2 torch==1.13.1
# copied these cells from my notebook - its a sentence transformer trained for
# sentence similarity with predict function and some data checks


def encode(samples):
    x = []
    model = SentenceTransformer(
        "/home/user12345/workspace/problemX/retriever_v6_20230901"
    )
    for s in samples:
        # not sure how to handle if the input is greater than the max input sequence
        # length
        vec = model.encode([s])[0]
        x.append(vec)
    return x


# a "data test"

embs = encode(["a", "a", "b"])
# if we normalise these embeddings maybe this might speed it up on large scale using
# dot product?
same_cos = cos_sim(embs[0], embs[1])
diff_cos = cos_sim(embs[0], embs[2])
# why does this have a rounding error - shouldn't this be determinstic?
assert isclose(same_cos, tensor(1.0000))

assert diff_cos < same_cos
print(same_cos, diff_cos)
