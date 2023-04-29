import json

import numpy as np
import requests

# post_data = {'inputs': []}

# input_name_0 = "prompt"
# input_datatype_0 = np.bytes_
# input_data_0 = "What state is Seattle in?"
# input_data_0_np = [str.encode(x) for x in input_data_0]
# print(input_data_0_np)
# input_shape_0 = [len(input_data_0)]
# triton_datatype_0 = "BYTES"

# input_name_1 = "max_length"
# input_shape_1 = [1]
# input_datatype_1 = np.int64
# input_data_1 = 100
# triton_datatype_1 = "UINT64"

# post_data['inputs'].append({
#     'name': input_name_0,
#     'shape': input_shape_0,
#     'datatype': triton_datatype_0,
#     'data': input_data_0_np})

# post_data['inputs'].append({
#     'name': input_name_1,
#     'shape': input_shape_1,
#     'datatype': triton_datatype_1,
#     'data': [input_data_1]})

# breakpoint()
# data=json.dumps(post_data)
# print(data)

# model_name = "google_flan_t5_small"
# result = requests.post(f"http://localhost:8000/v2/models/{model_name}/versions/1/infer",
#     data=json.dumps(post_data))

# print(result.json())


import tritonclient