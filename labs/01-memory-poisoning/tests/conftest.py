import pytest
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture(autouse=True)          # auto-apply to every test file
def mock_openai():
    """
    Replace the .create() call on *both* app instances
    (starter and solution) with a fast, deterministic stub.
    """
    from starter.app import main as vuln
    from solution.app import acl_main as secure

    dummy_resp = MagicMock()
    dummy_resp.choices = [
        MagicMock(message=MagicMock(content="DUMMY_RESPONSE"))
    ]

    # Create async mock that returns the dummy response
    async_mock = AsyncMock(return_value=dummy_resp)

    for mod in (vuln, secure):
        mod.client.chat.completions.create = async_mock

    yield                                           # run the test suite 