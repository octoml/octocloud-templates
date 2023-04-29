import enum

import numpy as np


# from
# https://github.com/triton-inference-server/common/blob/main/protobuf/model_config.proto
class ModelConfigDataTypes(enum.Enum):
    """These types are used in config.pbtxt."""

    TYPE_INVALID = 0
    TYPE_BOOL = 1
    TYPE_UINT8 = 2
    TYPE_UINT16 = 3
    TYPE_UINT32 = 4
    TYPE_UINT64 = 5
    TYPE_INT8 = 6
    TYPE_INT16 = 7
    TYPE_INT32 = 8
    TYPE_INT64 = 9
    TYPE_FP16 = 10
    TYPE_FP32 = 11
    TYPE_FP64 = 12
    TYPE_STRING = 13


_config_type_to_api = {
    "TYPE_BOOL": "BOOL",
    "TYPE_UINT8": "UINT8",
    "TYPE_UINT16": "UINT16",
    "TYPE_UINT32": "UINT32",
    "TYPE_UINT64": "UINT64",
    "TYPE_INT8": "INT8",
    "TYPE_INT16": "INT16",
    "TYPE_INT32": "INT32",
    "TYPE_INT64": "INT64",
    "TYPE_FP16": "FP16",
    "TYPE_FP32": "FP32",
    "TYPE_FP64": "FP64",
    "TYPE_STRING": "BYTES",
}

# Values from
# https://github.com/triton-inference-server/common/blob/main/protobuf/model_config.proto


class ModelInstanceGroup(enum.Enum):
    KIND_AUTO = 0
    KIND_GPU = 1
    KIND_CPU = 2
    KIND_MODEL = 3


# Function grabbed from
# https://github.com/triton-inference-server/client/blob/main/src/python/library/tritonclient/utils/__init__.py#L127
# Copied so that consumers of docker_package_ort do not need to pull in tritonclient.
def np_to_triton_api_type(np_dtype):
    if np_dtype == bool:
        return "BOOL"
    elif np_dtype == np.int8:
        return "INT8"
    elif np_dtype == np.int16:
        return "INT16"
    elif np_dtype == np.int32:
        return "INT32"
    elif np_dtype == np.int64:
        return "INT64"
    elif np_dtype == np.uint8:
        return "UINT8"
    elif np_dtype == np.uint16:
        return "UINT16"
    elif np_dtype == np.uint32:
        return "UINT32"
    elif np_dtype == np.uint64:
        return "UINT64"
    elif np_dtype == np.float16:
        return "FP16"
    elif np_dtype == np.float32:
        return "FP32"
    elif np_dtype == np.float64:
        return "FP64"
    elif np_dtype == np.object_ or np_dtype == np.bytes_:
        return "BYTES"
    return None


def np_to_triton_config_type(np_dtype):
    if np_dtype == bool:
        return "TYPE_BOOL"
    elif np_dtype == np.int8:
        return "TYPE_INT8"
    elif np_dtype == np.int16:
        return "TYPE_INT16"
    elif np_dtype == np.int32:
        return "TYPE_INT32"
    elif np_dtype == np.int64:
        return "TYPE_INT64"
    elif np_dtype == np.uint8:
        return "TYPE_UINT8"
    elif np_dtype == np.uint16:
        return "TYPE_UINT16"
    elif np_dtype == np.uint32:
        return "TYPE_UINT32"
    elif np_dtype == np.uint64:
        return "TYPE_UINT64"
    elif np_dtype == np.float16:
        return "TYPE_FP16"
    elif np_dtype == np.float32:
        return "TYPE_FP32"
    elif np_dtype == np.float64:
        return "TYPE_FP64"
    elif np_dtype == np.object_ or np_dtype == np.bytes_:
        return "TYPE_STRING"
    return None


def model_config_to_api(model_config_dtype: str) -> str:
    """Converts config.pbtxt data type names to what the Triton API expects.

    :return: the the Triton API name for the given model config data type.
    """
    return _config_type_to_api[model_config_dtype]


def api_to_model_config(api_type: str) -> str:
    """Converts Triton API names to model config data types.

    :return: the model config data type for the Triton API name.
    """
    api_to_config_type = {v: k for k, v in _config_type_to_api.items()}
    return api_to_config_type[api_type]


class TritonPort(enum.Enum):
    """Triton has three ports for interaction."""

    HTTP = 8000
    GRPC = 8001
    METRICS = 8002
    SAGEMAKER = 8080
