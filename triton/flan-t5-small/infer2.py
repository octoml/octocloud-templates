import numpy as np
import tritonclient.grpc as grpc_client

model_name = "google_flan_t5_small"
prompt_text = "What state is Seattle in?"

client = grpc_client.InferenceServerClient("localhost:8001")

if client.is_server_ready():
    print("Server is ready")

# model_config = client.get_model_config(model_name=model_name)


prompt_np = np.array([str.encode(prompt_text)], dtype=np.object_)
prompt = grpc_client.InferInput(name="prompt", shape=[1], datatype="BYTES")
prompt.set_data_from_numpy(prompt_np)

max_length_np = np.array([100], dtype=np.uint64)
max_length = grpc_client.InferInput(name="max_length", shape=[1], datatype="UINT64")
max_length.set_data_from_numpy(max_length_np)

inputs = [prompt, max_length]

output0 = grpc_client.InferRequestedOutput(name="output")
outputs = [output0]

response = client.infer(
    model_name=model_name, model_version="1", inputs=inputs, outputs=outputs
)

breakpoint()
print(response)


# client.infer(model_name=model_name, model_version="1", inputs=inputs, outputs=outputs)
