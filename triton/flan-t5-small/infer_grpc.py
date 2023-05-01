import numpy as np
import tritonclient.grpc as grpc_client

from triton.utils.triton_utils import get_stats_time_ms

model_name = "google_flan_t5_small"
prompt_text = "What state is Seattle in?"

client = grpc_client.InferenceServerClient("localhost:8001")

if client.is_server_ready():
    print("Server is ready")

# First define the input and output tensors
prompt = grpc_client.InferInput(name="prompt", shape=[1], datatype="BYTES")
max_length = grpc_client.InferInput(name="max_length", shape=[1], datatype="UINT64")
output0 = grpc_client.InferRequestedOutput(name="output")

# Next generate some test data
prompt_np = np.array([str.encode(prompt_text, encoding="utf-8")], dtype=np.object_)
max_length_np = np.array([100], dtype=np.uint64)

for i in range(100):
    prompt.set_data_from_numpy(prompt_np)
    max_length.set_data_from_numpy(max_length_np)

    inputs = [prompt, max_length]
    outputs = [output0]

    response = client.infer(model_name=model_name, inputs=inputs, outputs=outputs)
    response_text = response.as_numpy("output")[0].decode("utf-8")

    print(response_text)

# Read inference metrics
stats = client.get_inference_statistics(model_name=model_name, as_json=True)

istats = stats["model_stats"][0]["inference_stats"]
compute_input_ms = get_stats_time_ms(istats["compute_input"])
compute_infer_ms = get_stats_time_ms(istats["compute_infer"])
compute_output_ms = get_stats_time_ms(istats["compute_output"])

print(f"compute_input  = {float('%.3g' % compute_input_ms)} ms")
print(f"compute_infer  = {float('%.3g' % compute_infer_ms)} ms")
print(f"compute_output = {float('%.3g' % compute_output_ms)} ms")
