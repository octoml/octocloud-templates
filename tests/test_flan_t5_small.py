import json
import pathlib
import subprocess
import time
import uuid

from utils import get_container_ip_address


def test_container():
    model = "flan-t5-small"
    path = pathlib.Path(__file__).parent.parent
    tag = uuid.uuid4().hex

    # Build the model container and tag it with a custom hash
    cmd = f"docker build -t {tag} -f {path}/{model}/Dockerfile {path}/{model}"
    result = subprocess.run(cmd.split(" "), capture_output=True)
    assert result.returncode == 0

    # Launch the container
    cmd = f"docker run -d --rm -p 8000:8000 --env SERVERPORT=8000 -t {tag}"
    result = subprocess.run(cmd.split(" "), capture_output=True)
    assert result.returncode == 0
    server_hash = result.stdout.decode("utf-8").strip()
    server_ip = get_container_ip_address(server_hash)

    time.sleep(5)

    cmd = [
        "curl",
        "-X",
        "POST",
        f"http://{server_ip}:8000/predict",
        "-H",
        '"Content-Type: application/json"',
        "--data",
        '{"prompt":"What state is Seattle in?","max_length":100}',
    ]

    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0
    result_json = json.loads(result.stdout.decode("utf-8").strip())
    assert "completion" in result_json.keys()
    assert result_json["completion"] == "Seattle"

    cmd = f"docker container stop {server_hash}"
    result = subprocess.run(cmd.split(" "), capture_output=True)
    assert result.returncode == 0
