import enum
import re
import typing

from triton.utils.triton_types import ModelInstanceGroup

_OCTOML_VERSION = "1.0.0"
_TAG_FORMAT = "quay.io/octoml/model-server:{}-{}-{}"


class TensorDetail(typing.NamedTuple):
    name: str
    """Tensor name."""

    shape: typing.Sequence[int]
    """Tensor shape."""

    triton_config_dtype: str
    """Tensor dtype."""


class InstanceGroup(typing.NamedTuple):
    kind: ModelInstanceGroup
    """Kind of instance group"""


class BackendType(enum.Enum):
    """Type of backend for the model"""

    PYTHON = "python"
    TENSORFLOW = "tensorflow"
    ONNXRUNTIME = "onnxruntime"
    TENSORRT = "tensorrt"
    PYTORCH = "pytorch"
    TVM = "python"
    ENSEMBLE = "ensemble"


class HardwarePlatform(enum.Enum):
    """Hardware platforms supported by Docker."""

    LINUX_X86_64 = "linux/x86_64"
    LINUX_ARM64 = "linux/arm64"
    LINUX_ARM32 = "linux/arm32"


class GPUSupport(enum.Enum):
    """GPU platforms supported by Docker."""

    NONE = "cpu"
    CUDA = "cuda"
    # ... eventually, VULKAN = "vulkan"


class PlatformType(enum.Enum):
    """Type of platform for the model.

    From
    https://github.com/triton-inference-server/backend/blob/main/README.md#backends.
    """

    TENSORRT = "tensorrt_plan"
    PYTORCH = "pytorch_libtorch"
    ONNXRUNTIME = "onnxruntime_onnx"
    TENSORFLOW_GRAPHDEF = "tensorflow_graphdef"
    TENSORFLOW_SAVEDMODEL = "tensorflow_savedmodel"


def build_triton_config(
    model_name: str,
    inputs: typing.Sequence[TensorDetail],
    outputs: typing.Sequence[TensorDetail],
    backend: typing.Optional[BackendType] = None,
    platform: typing.Optional[PlatformType] = None,
    backend_config: typing.List[str] = [],
    instance_group: typing.Optional[InstanceGroup] = None,
    metadata: typing.Optional[typing.Dict[str, str]] = {},
) -> str:
    """This function builds a model-specific config.pbtxt file required by triton.
    The file is built in a specific directory location to satisfy triton.

    :param inputs: information about the model inputs.
    :param ouptuts: information about the model outputs.
    :param backend: the backend on which this model runs.
    :return: string containing the constructed config.pbtxt
    """
    if not backend and not platform:
        raise ValueError("Must set either platform or backend")
    if backend and platform:
        raise ValueError("Must set only one of platform or backend")
    config = f'name: "{model_name}"\n'
    if platform:
        config += f'platform: "{platform.value}"\n'
    elif backend:
        config += f'backend: "{backend.value}"\n'
    config += "input ["
    item_separator = ""
    for input_item in inputs:
        dtype = input_item.triton_config_dtype
        config += f"{item_separator}\n  {{\n"
        config += f'    name: "{input_item.name}"\n'
        config += f"    data_type: {dtype}\n"
        for dim in input_item.shape:
            config += f"    dims: {int(dim)}\n"
        config += "  }"
        item_separator = ","
    config += "\n]\n"
    config += "output ["
    item_separator = ""

    for output_item in outputs:
        dtype = output_item.triton_config_dtype
        config += f"{item_separator}\n  {{\n"
        config += f'    name: "{output_item.name}"\n'
        config += f"    data_type: {dtype}\n"
        for dim in output_item.shape:
            config += f"    dims: {int(dim)}\n"
        config += "  }"
        item_separator = ","
    config += "\n]\n"
    if instance_group:
        config += f"instance_group [ {{ kind: {instance_group.kind.name} }} ]"
    for bc in backend_config:
        config += bc + "\n"
    for k, v in metadata.items():
        parameter = 'parameters { key: "%s" value: { string_value: "%s" }}' % (
            k,
            v,
        )
        config += parameter + "\n"
    return config


def sanitize_model_name(model_name: str):
    """Make the supplied model name python wheel friendly."""
    return re.sub(r"[^\w]", "_", model_name)
