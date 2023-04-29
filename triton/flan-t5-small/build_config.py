import argparse

from triton.utils.triton_utils import (
    BackendType,
    TensorDetail,
    build_triton_config,
    sanitize_model_name,
)

_MODEL_NAME = "google/flan-t5-small"


def build():
    prompt = TensorDetail("prompt", [-1], "TYPE_STRING")
    max_length = TensorDetail("max_length", [1], "TYPE_UINT64")
    output = TensorDetail("output", [-1], "TYPE_STRING")

    config = build_triton_config(
        model_name=sanitize_model_name(_MODEL_NAME),
        inputs=[prompt, max_length],
        outputs=[output],
        backend=BackendType.PYTHON,
    )
    print(config)


def main():
    """Entry point for interacting with this model via CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    build()


if __name__ == "__main__":
    main()
