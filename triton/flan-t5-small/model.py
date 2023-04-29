import importlib
import json

import torch

# triton_python_backend_utils is available in every Triton Python model. You
# need to use this module to create inference requests and responses. It also
# contains some utility functions for extracting information from model_config
# and converting Triton input/output types to numpy types.
import triton_python_backend_utils as pb_utils
from transformers import T5ForConditionalGeneration, T5Tokenizer

_MODEL_NAME = "google/flan-t5-small"
"""The model's name on HuggingFace."""

_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
"""Device on which to serve the model."""


class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to intialize any state associated with this model.
        Parameters
        ----------
        args : dict
            Both keys and values are strings. The dictionary keys and values are:
            * model_config: A JSON string containing the model configuration
            * model_instance_kind: A string containing model instance kind
            * model_instance_device_id: A string containing model instance device ID
            * model_repository: Model repository path
            * model_version: Model version
            * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        self.model_config = model_config = json.loads(args["model_config"])

        self.model_name = model_config["name"]

        self.inputs = model_config["input"]
        self.outputs = model_config["output"]

        self.input_names = [i["name"] for i in self.inputs]
        self.output_names = [o["name"] for o in self.outputs]
        self.output_numpy_dtypes = [
            pb_utils.triton_string_to_numpy(o["data_type"]) for o in self.outputs
        ]

        # Fetch the model
        self._tokenizer = T5Tokenizer.from_pretrained(_MODEL_NAME)
        self._model = T5ForConditionalGeneration.from_pretrained(_MODEL_NAME).to(
            _DEVICE
        )

    def execute(self, requests):
        """`execute` MUST be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference request is made
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse
        Parameters
        ----------
        requests : list
            A list of pb_utils.InferenceRequest
        Returns
        -------
        list
            A list of pb_utils.InferenceResponse. The length of this list must
            be the same as `requests`
        """

        responses = []

        # Every Python backend must iterate over every one of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for request in requests:
            # First create a list of TVM inputs inputs
            input_list = []
            # for input_name in self.input_names:
            #     input_tensor = pb_utils.get_input_tensor_by_name(request, input_name)
            #     input_list.append(tvm.nd.array(input_tensor.as_numpy()))

            # output_list = self.model.run(*input_list)
            prompt = pb_utils.get_input_tensor_by_name(request, "prompt")
            max_length = pb_utils.get_input_tensor_by_name(request, "max_length")

            input_ids = self._tokenizer(prompt, return_tensors="pt").input_ids.to(
                _DEVICE
            )
            output = self._model.generate(input_ids, max_length=max_length)
            result = self._tokenizer.decode(output[0], skip_special_tokens=True)

            output_tensors = []
            for output_tensor, output_name, output_dtype in zip(
                output_list, self.output_names, self.output_numpy_dtypes
            ):
                output_tensor = pb_utils.Tensor(output_name, output_tensor.asnumpy())
                output_tensors.append(output_tensor)

            # Create InferenceResponse. You can set an error here in case
            # there was a problem with handling this inference request.
            # Below is an example of how you can set errors in inference
            # response:
            #
            # pb_utils.InferenceResponse(
            #    output_tensors=..., TritonError("An error occured"))
            inference_response = pb_utils.InferenceResponse(
                output_tensors=output_tensors
            )
            responses.append(inference_response)

        # You should return a list of pb_utils.InferenceResponse. Length
        # of this list must match the length of `requests` list.
        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        pass
