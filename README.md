# Sentence Transformer Model Serving

This is a torch model serving repository for a fine-tuned `microsoft/mpnet-base`
Sentence Transformer model, which allows to calculate sentence embeddings.

There is a model provided within this repository (`data/model`) which has been
fine-tuned on Reddit data.

## Prerequisites

The easiest way to run inference using this repository is when you have the following
prerequisites installed:

- `Task` (installation guide: https://taskfile.dev/installation/)
- `Docker` (installation guide: https://docs.docker.com/engine/install/)

After installing these, one can locate the sentence data to do inference on and the
model to do inference with in the following locations:

- Sentence (meta)data: `data/texts_{doc_id}.json`
- Pages data: `data/pages_{doc_id}.csv`
- Sentence Transformer Model: `data/model`

An example of how to store this data and model is provided in this repository.

## Run the Model Serving Application

Once these prerequisites are met, one can build the image by running:

```bash
task build_image
```

Followed by the following command, which will run the code in `script.py`
which is being executed in the container:

```bash
task run_script
```

During execution of this step, the logs will be outputted to your terminal. After
`script.py` is done executing, the container will exit and remove itself.

In case of a runtime error, one can stop the container by running:

```bash
task stop_container
```

## Running on GPU vs CPU

The inference code will detect whenever a GPU is available, so if the image is
built on a machine with a GPU, one can simply uncomment the `deploy:` part in
the `docker-compose.yml` file and run `task run_script` again. This will
significantly speed up inference. For comparison: on a `G5-XLarge` AWS instance,
the `task run_script` task takes 8 seconds to complete, whilst on a CPU this is
closer to 8 minutes.

## Run the development environment

To run a development python environment (non-dockerized), one can run (requires
`poetry 1.4.2` to be installed):

```bash
task prep_env
```

This environment can be used for e.g. for your IDE.

## Run the tests in docker

The development image is different from the production image in that it also has
the development dependencies installed (e.g. pytest).

```bash
task build_dev_image
```

Tests are ran by running the following command. The files `./src` and `./tests` are
mounted into the development container.

```bash
task run_tests
```

## Improvements to the repo:

- Next step would be to integrate with Github Actions for testing, linting and
formatting checks. At the moment the repo is set up for local development.  The idea
here would stay the same: a multi-stage docker build which can produce a production
image and a development image. The production image is used for serving the model,
with the necessary data and models mounted in it. The development image is used for
running testing, linting and formatting checks (with either the code and the tests
mounted or copied in it) and has more dependencies installed (e.g. ruff, pytest, etc.)
- Error handling. There's app specific error handling done at the moment.
- Data validation. The data in the pages and texts files are not validated at the
moment. While loading this data, we could perform validation checks to make sure
we're feeding sensible data to the model.
- Write (better) unit and integration tests.
- Model tests: We can construct test scenarios where model performance
is tested, e.g. the distance between the embeddings of two sentences with a similar
semantic meaning should be within an acceptable range.
- We can look into improving the speed of the SentenceTransformer model on CPU. This
is now fairly slow. There are multiple things we could experiment with: quantising the
model, multiprocessing strategies, model serving frameworks like BentoML or TorchServe,
etc.
- When the data to do inference on would become too large to hold in memory (or
if the memory constraints would be tightened), we could use a generator to yield the
data in batches from the source (instead of loading the full file in memory at once).
- We could also consider storing the sentences and their metadata in a PostgreSQL
database, if we would need more robust data storage compared to files.
- We could consider storing the vectors in a Vector Database instead of simply
returning/printing them out.
- etc.
