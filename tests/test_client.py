import httpx
import pytest
import respx

from jambonz import JambonzClient, AsyncJambonzClient
from jambonz.exceptions import (
    JambonzAuthError,
    JambonzNotFoundError,
    JambonzRateLimitError,
    JambonzValidationError,
    JambonzAPIError,
)
from jambonz.models import Carrier, PhoneNumber, Application, SpeechService, Call
from tests.conftest import ACCOUNT_SID, BASE_URL


class TestClientInit:
    def test_context_manager(self, mock_api):
        with JambonzClient(account_sid="a", api_key="k", base_url=BASE_URL) as c:
            assert c.account_sid == "a"

    def test_reads_env_vars(self, monkeypatch, mock_api):
        monkeypatch.setenv("JAMBONZ_ACCOUNT_SID", "env-sid")
        monkeypatch.setenv("JAMBONZ_API_KEY", "env-key")
        monkeypatch.setenv("JAMBONZ_BASE_URL", BASE_URL)
        c = JambonzClient()
        assert c.account_sid == "env-sid"
        c.close()

    def test_auth_header(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(200, json=[])
        )
        client.carriers.list()
        request = mock_api.calls[0].request
        assert request.headers["authorization"] == "Bearer test-api-key"


class TestRequestHooks:
    def test_on_request_called(self, mock_api):
        calls = []
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(200, json=[])
        )
        c = JambonzClient(
            account_sid=ACCOUNT_SID,
            api_key="k",
            base_url=BASE_URL,
            on_request=lambda req: calls.append(req.url),
        )
        c.carriers.list()
        assert len(calls) == 1
        c.close()


class TestExceptions:
    def test_401_raises_auth_error(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"})
        )
        with pytest.raises(JambonzAuthError) as exc_info:
            client.carriers.list()
        assert exc_info.value.status_code == 401

    def test_404_raises_not_found(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers/99999999-9999-9999-9999-999999999999").mock(
            return_value=httpx.Response(404, json={"error": "not found"})
        )
        with pytest.raises(JambonzNotFoundError):
            client.carriers.get("99999999-9999-9999-9999-999999999999")

    def test_422_raises_validation_error(self, client, mock_api):
        mock_api.post(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(422, json={"error": "invalid"})
        )
        with pytest.raises(JambonzValidationError):
            client.carriers.create(name="bad")

    def test_429_raises_rate_limit(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(429, json={"error": "too many"})
        )
        with pytest.raises(JambonzRateLimitError):
            client.carriers.list()

    def test_500_raises_api_error(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(500, text="internal error")
        )
        with pytest.raises(JambonzAPIError) as exc_info:
            client.carriers.list()
        assert exc_info.value.status_code == 500


class TestCarriers:
    CARRIER_JSON = {
        "voip_carrier_sid": "11111111-1111-1111-1111-111111111111",
        "name": "telnyx",
        "is_active": True,
        "trunk_type": "static_ip",
    }

    def test_list(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(200, json=[self.CARRIER_JSON])
        )
        carriers = client.carriers.list()
        assert len(carriers) == 1
        assert isinstance(carriers[0], Carrier)
        assert carriers[0].name == "telnyx"

    def test_get(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers/11111111-1111-1111-1111-111111111111").mock(
            return_value=httpx.Response(200, json=self.CARRIER_JSON)
        )
        carrier = client.carriers.get("11111111-1111-1111-1111-111111111111")
        assert str(carrier.voip_carrier_sid) == "11111111-1111-1111-1111-111111111111"
        assert carrier.name == "telnyx"

    def test_create(self, client, mock_api):
        mock_api.post(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(201, json=self.CARRIER_JSON)
        )
        carrier = client.carriers.create(name="telnyx", trunk_type="static_ip")
        assert carrier.name == "telnyx"

    def test_update(self, client, mock_api):
        updated = {**self.CARRIER_JSON, "name": "telnyx-updated"}
        mock_api.put(f"Accounts/{ACCOUNT_SID}/VoipCarriers/11111111-1111-1111-1111-111111111111").mock(
            return_value=httpx.Response(200, json=updated)
        )
        carrier = client.carriers.update("11111111-1111-1111-1111-111111111111", name="telnyx-updated")
        assert carrier.name == "telnyx-updated"

    def test_delete(self, client, mock_api):
        mock_api.delete(f"Accounts/{ACCOUNT_SID}/VoipCarriers/11111111-1111-1111-1111-111111111111").mock(
            return_value=httpx.Response(204)
        )
        client.carriers.delete("11111111-1111-1111-1111-111111111111")



class TestPhoneNumbers:
    NUMBER_JSON = {
        "phone_number_sid": "22222222-2222-2222-2222-222222222222",
        "number": "34931228497",
        "voip_carrier_sid": "11111111-1111-1111-1111-111111111111",
        "application_sid": "33333333-3333-3333-3333-333333333333",
    }

    def test_list(self, client, mock_api):
        mock_api.get("PhoneNumbers").mock(
            return_value=httpx.Response(200, json=[self.NUMBER_JSON])
        )
        numbers = client.phone_numbers.list()
        assert len(numbers) == 1
        assert isinstance(numbers[0], PhoneNumber)
        assert numbers[0].number == "34931228497"

    def test_create(self, client, mock_api):
        mock_api.post("PhoneNumbers").mock(
            return_value=httpx.Response(201, json=self.NUMBER_JSON)
        )
        pn = client.phone_numbers.create(number="34931228497", voip_carrier_sid="11111111-1111-1111-1111-111111111111")
        assert pn.number == "34931228497"


class TestApplications:
    APP_JSON = {
        "application_sid": "33333333-3333-3333-3333-333333333333",
        "name": "testfastapi",
        "call_hook": "https://example.com/call",
    }

    def test_list(self, client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/Applications").mock(
            return_value=httpx.Response(200, json=[self.APP_JSON])
        )
        apps = client.applications.list()
        assert len(apps) == 1
        assert isinstance(apps[0], Application)
        assert apps[0].name == "testfastapi"


class TestRetry:
    def test_retries_on_429(self, mock_api):
        path = f"Accounts/{ACCOUNT_SID}/VoipCarriers"
        mock_api.get(path).mock(
            side_effect=[
                httpx.Response(429, headers={"Retry-After": "0"}, json={}),
                httpx.Response(200, json=[]),
            ]
        )
        c = JambonzClient(
            account_sid=ACCOUNT_SID,
            api_key="k",
            base_url=BASE_URL,
            max_retries=1,
        )
        carriers = c.carriers.list()
        assert carriers == []
        assert mock_api.calls.call_count == 2
        c.close()

    def test_retries_on_500(self, mock_api):
        path = f"Accounts/{ACCOUNT_SID}/VoipCarriers"
        mock_api.get(path).mock(
            side_effect=[
                httpx.Response(500, text="error"),
                httpx.Response(200, json=[]),
            ]
        )
        c = JambonzClient(
            account_sid=ACCOUNT_SID,
            api_key="k",
            base_url=BASE_URL,
            max_retries=1,
        )
        carriers = c.carriers.list()
        assert carriers == []
        c.close()


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_list_carriers(self, async_client, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(200, json=[{"voip_carrier_sid": "44444444-4444-4444-4444-444444444444", "name": "test"}])
        )
        carriers = await async_client.carriers.list()
        assert len(carriers) == 1
        assert carriers[0].name == "test"
        await async_client.close()

    @pytest.mark.asyncio
    async def test_async_context_manager(self, mock_api):
        mock_api.get(f"Accounts/{ACCOUNT_SID}/VoipCarriers").mock(
            return_value=httpx.Response(200, json=[])
        )
        async with AsyncJambonzClient(
            account_sid=ACCOUNT_SID, api_key="k", base_url=BASE_URL
        ) as c:
            carriers = await c.carriers.list()
            assert carriers == []
