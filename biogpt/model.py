"""Model wrapper for serving ."""
import argparse
import typing

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_MODEL_NAME = "microsoft/biogpt-large"
_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"

class Model:
    """Wrapper for a Text Generation model."""

    def __init__(self):
        """Initialize the model."""
        self._tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        self._model = AutoModelForCausalLM.from_pretrained(_MODEL_NAME).to(_DEVICE)

    def _decode(self, token_ids):
        return ' '.join([self._tokenizer.decode(x) for x in token_ids['input_ids']])
    
    def predict(self, inputs: typing.Dict[str, typing.Union[str, int]]) -> typing.Dict[str, str]:
        """Return a dict containing the completion of the given prompt.

        :param inputs: dict of inputs containing a prompt and optionally the max length
            of the completion to generate.
        :return: a dict containing the generated completion.
        """
        prompt = inputs.get("prompt", None)
        max_length = inputs.get("max_length", 512)

        input_ids = self._tokenizer(prompt, return_tensors="pt").input_ids.to(_DEVICE)
        results = self._model.generate(input_ids, max_length=max_length, num_return_sequences=5, do_sample=True)

        return {f"result_{i+1}": self._tokenizer.decode(result.squeeze(), skip_special_tokens=True) 
                for i, result in enumerate(results)}

    @classmethod
    def fetch(cls) -> None:
        """Pre-fetches the model for implicit caching by Transformers."""
        cls()

def main():
    """Entry point for interacting with this model via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    if args.fetch:
        Model.fetch()
    
    #model = Model()
    #print(model.predict(inputs={"prompt": "COVID-19 is"}))

if __name__ == "__main__":
    main()
