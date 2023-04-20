"""Model wrapper for serving flan-t5-small."""

import argparse
import typing

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

_MODEL_NAME = "google/flan-t5-small"
"""The model's name on HuggingFace."""

_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
"""Device on which to serve the model."""


class Model:
    """Wrapper for T5 Text Generation model."""

    def __init__(self):
        """Initialize the model."""
        self._tokenizer = T5Tokenizer.from_pretrained(_MODEL_NAME)
        self._model = T5ForConditionalGeneration.from_pretrained(_MODEL_NAME).to(
            _DEVICE
        )

    def predict(self, inputs: typing.Dict[str, str]) -> typing.Dict[str, str]:
        """Return a dict containing the completion of the given prompt.

        :param inputs: dict of inputs containing a prompt and optionally the max length
            of the completion to generate.
        :return: a dict containing the generated completion.
        """
        prompt = inputs.get("prompt", None)
        max_length = inputs.get("max_length", 2048)

        input_ids = self._tokenizer(prompt, return_tensors="pt").input_ids.to(_DEVICE)
        output = self._model.generate(input_ids, max_length=max_length)
        result = self._tokenizer.decode(output[0], skip_special_tokens=True)

        return {"completion": result}

    @classmethod
    def fetch(cls) -> None:
        """Pre-fetches the model for implicit caching by Transfomers."""
        # Running the constructor is enough to fetch this model.
        cls()


def main():
    """Entry point for interacting with this model via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    if args.fetch:
        Model.fetch()


if __name__ == "__main__":
    main()
