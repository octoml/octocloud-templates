"""Test sample utility for FILM API"""

import argparse
import base64
import json
import logging

logger = logging.getLogger("__name__")


def generate(frame_paths: str, json_file_path: str, times_to_interpolate: str):
    """Generate a JSON file containing a test sample for FILM API"""

    data = {
        "times_to_interpolate": times_to_interpolate,
    }

    for idx, image_path in enumerate(frame_paths):
        try:
            with open(image_path, "rb") as fid:
                # frame index start at 0
                data[f"frame_{idx}"] = base64.b64encode(fid.read()).decode(
                    "utf-8"
                )  # base64 image string
        except Exception as e:
            logger.error(f"Error: Could not encode image files in {image_path}! \n {e}")
            raise

    with open(json_file_path, "w") as f:
        json.dump(data, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frame-paths", nargs="+", default=["../assets/start.png", "../assets/end.png"]
    )
    parser.add_argument("--json-file", default="test_sample.json")
    parser.add_argument("--times-to-interpolate", default="7")
    args = parser.parse_args()

    generate(args.frame_paths, args.json_file, args.times_to_interpolate)


if __name__ == "__main__":
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()
