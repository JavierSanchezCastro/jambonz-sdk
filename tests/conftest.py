import httpx
import pytest
import respx

from jambonz import JambonzClient, AsyncJambonzClient

ACCOUNT_SID = "test-account-sid"
API_KEY = "test-api-key"
BASE_URL = "https://jambonz.test"


@pytest.fixture
def mock_api():
    with respx.mock(base_url=f"{BASE_URL}/v1/") as mock:
        yield mock


@pytest.fixture
def client(mock_api):
    c = JambonzClient(
        account_sid=ACCOUNT_SID,
        api_key=API_KEY,
        base_url=BASE_URL,
        max_retries=0,
    )
    yield c
    c.close()


@pytest.fixture
def async_client(mock_api):
    c = AsyncJambonzClient(
        account_sid=ACCOUNT_SID,
        api_key=API_KEY,
        base_url=BASE_URL,
        max_retries=0,
    )
    return c
