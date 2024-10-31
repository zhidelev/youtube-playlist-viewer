import pytest
import schemathesis

# Globally enable OpenAPI 3.1 experimental feature
schemathesis.experimental.OPEN_API_3_1.enable()

schema = schemathesis.from_uri(
    "http://127.0.0.1:8000/openapi.json",
)


@pytest.mark.auto_generated
@schema.parametrize()
def test_api(case):
    case.call_and_validate()
