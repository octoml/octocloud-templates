"""Model wrapper for serving diffusers model."""

import argparse
import typing

import torch
from diffusers import StableDiffusionPipeline

import base64
from io import BytesIO

_MODEL_NAME = "prompthero/openjourney"
"""The model's name on HuggingFace."""

_DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
"""Device on which to serve the model."""


class Model:
    """Wrapper for diffusers model."""

    def __init__(self):
        """Initialize the model."""
        self._pipe = StableDiffusionPipeline.from_pretrained(_MODEL_NAME, torch_dtype=torch.float16).to(_DEVICE)

    def predict(self, inputs: typing.Dict[str, str]) -> typing.Dict[str, str]:
        """Return a dict containing the completion of the given prompt.

        :param inputs: dict of inputs containing a prompt and optionally the max length
            of the completion to generate.
        :return: a dict containing the generated completion.
        """
        prompt = inputs.get("prompt", None)
        
        output = self._pipe(prompt).images[0]
        im_file = BytesIO()
        output.save(im_file, format="PNG")
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes).decode("utf-8")

        return {"completion": im_b64}

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
