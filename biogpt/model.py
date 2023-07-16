"""Model wrapper for serving ."""
import argparse
import typing

import torch
#from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from transformers import BioGptTokenizer
from transformers import BioGptForCausalLM



_MODEL_NAME = "microsoft/BioGPT-Large"
"""The model's name on HuggingFace."""

_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
"""Device on which to serve the model."""


class Model:
    """Wrapper for a  Text Generation model."""

    def __init__(self):
        """Initialize the model."""
        self._tokenizer = BioGptTokenizer.from_pretrained(_MODEL_NAME)
        self._model = BioGptForCausalLM.from_pretrained(_MODEL_NAME).to(
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
        #output = self._model.generate(input_ids, max_length=max_length)
        #result = self._tokenizer.decode(output[0], skip_special_tokens=True)
        #loss = outputs.loss
        #logits = outputs.logits
        result = self._model(**input_ids)
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