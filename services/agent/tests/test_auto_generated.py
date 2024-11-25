import pytest
import schemathesis
import subprocess
import requests
import time


OPENAPI_URL = "http://127.0.0.1:8000/openapi.json"

# Globally enable OpenAPI 3.1 experimental feature
schemathesis.experimental.OPEN_API_3_1.enable()

pytestmark = [pytest.mark.auto_generated, pytest.mark.slow]

@pytest.fixture(scope="module", autouse=True)
def run_docker_compose():
    res = subprocess.run(["docker", "compose", "up", "-d"], capture_output=True, text=True)
    print(res.stdout)
    print(res.stderr)
    init_time = time.time()

    while True:
        if time.time() - init_time > 60:
            break

        try:
            requests.get(OPENAPI_URL)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            continue
        else:
            break

    yield schemathesis.from_uri(OPENAPI_URL)

    subprocess.run(["docker", "compose", "down"])

schema = schemathesis.from_pytest_fixture(
    "run_docker_compose",
)

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
