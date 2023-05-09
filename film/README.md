This subrepo describes how to use the FILM interpolation template on the OctoML compute service.

## Introduction

FILM is a model for generating intermediate frames between two existing frames in a video sequence. On the OctoML compute service Templates page[https://octoai.cloud/templates], we give you an easy button to obtain a production-grade endpoint for this model.


## Requirements
Make sure you have at least two images in your working directory that you want to interpolate between, and have installed Python3 on your device. 
In this repo, we offer image1.jpg and image2.jpg as example inputs.

## Cloning the template

Go to the Templates [page](https://octoai.cloud/templates) on the OctoML compute service, locate the "film-demo" template, and click Clone Template. That brings up a modal where you can confirm the settings for your endpoint; click "Clone" in the modal to proceed. Now you'll see an Endpoint URL on the page for your new endpoint.

## Using the endpoint
First, run `python3 generate_test_sample.py --frame-paths image1.jpg image2.jpg --json-file data.json --times-to-interpolate 7` to construct a JSON file as input to the endpoint.

Then, run a CURL in your command line against the endpoint: `curl -X POST "<Endpoint URL>" -H "Content-Type: application/json" --data @data.json > result.json`

Finally, parse the output JSON by running `python3 parse_response.py`, and you'll see an mp4 file in your working directory.
