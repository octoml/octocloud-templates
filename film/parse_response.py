"""Utility to parse response from FILM API"""

import argparse
import base64
import json


def parse_video(json_file_path: str, output_file: str):
    """Parse JSON response from FILM API to a MP4 video file"""
    with open(json_file_path, "r") as fid:
        response = json.load(fid)

    with open(f"{output_file}", "wb") as fid:
        fid.write(base64.b64decode(response["video"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", default="response.json")
    parser.add_argument("--output-file", default="generated_video.mp4")
    args = parser.parse_args()

    parse_video(args.json_file, args.output_file)


if __name__ == "__main__":
    main()
