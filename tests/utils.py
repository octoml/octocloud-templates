import subprocess


def get_container_ip_address(container_hash: str) -> str:
    cmd = [
        "docker",
        "container",
        "inspect",
        container_hash,
        "--format",
        "{{.NetworkSettings.IPAddress}}",
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout.decode("utf-8").strip()
