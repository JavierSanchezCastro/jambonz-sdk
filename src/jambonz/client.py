from functools import cached_property
from typing import Callable

import httpx

from jambonz._base import BaseClient, AsyncBaseClient
from jambonz.resources.accounts import Accounts, AsyncAccounts
from jambonz.resources.api_keys import ApiKeys, AsyncApiKeys
from jambonz.resources.applications import Applications, AsyncApplications
from jambonz.resources.calls import Calls, AsyncCalls
from jambonz.resources.recent_calls import RecentCalls, AsyncRecentCalls
from jambonz.resources.carriers import Carriers, AsyncCarriers
from jambonz.resources.gateways import Gateways, AsyncGateways
from jambonz.resources.phone_numbers import PhoneNumbers, AsyncPhoneNumbers
from jambonz.resources.speech_services import SpeechServices, AsyncSpeechServices
from jambonz.resources.users import Users, AsyncUsers


class JambonzClient(BaseClient):
    """Synchronous jambonz API client.

    Usage:
        client = JambonzClient(account_sid="xxx", api_key="yyy")

        # Or with env vars JAMBONZ_ACCOUNT_SID, JAMBONZ_API_KEY
        client = JambonzClient()

        # As context manager
        with JambonzClient() as client:
            carriers = client.carriers.list()
    """

    def __init__(
        self,
        account_sid: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ):
        super().__init__(
            account_sid=account_sid,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            on_request=on_request,
            on_response=on_response,
        )

    # --- Platform Management ---

    @cached_property
    def accounts(self) -> Accounts:
        return Accounts(self)

    @cached_property
    def users(self) -> Users:
        return Users(self)

    @cached_property
    def api_keys(self) -> ApiKeys:
        return ApiKeys(self)

    @cached_property
    def carriers(self) -> Carriers:
        return Carriers(self)

    @cached_property
    def gateways(self) -> Gateways:
        return Gateways(self)

    @cached_property
    def phone_numbers(self) -> PhoneNumbers:
        return PhoneNumbers(self)

    @cached_property
    def applications(self) -> Applications:
        return Applications(self)

    @cached_property
    def speech_services(self) -> SpeechServices:
        return SpeechServices(self)

    # --- Call Control ---

    @cached_property
    def calls(self) -> Calls:
        return Calls(self)

    @cached_property
    def recent_calls(self) -> RecentCalls:
        return RecentCalls(self)


class AsyncJambonzClient(AsyncBaseClient):
    """Async jambonz API client.

    Usage:
        async with AsyncJambonzClient() as client:
            carriers = await client.carriers.list()
    """

    def __init__(
        self,
        account_sid: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        on_request: Callable[[httpx.Request], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ):
        super().__init__(
            account_sid=account_sid,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            on_request=on_request,
            on_response=on_response,
        )

    # --- Platform Management ---

    @cached_property
    def accounts(self) -> AsyncAccounts:
        return AsyncAccounts(self)

    @cached_property
    def users(self) -> AsyncUsers:
        return AsyncUsers(self)

    @cached_property
    def api_keys(self) -> AsyncApiKeys:
        return AsyncApiKeys(self)

    @cached_property
    def carriers(self) -> AsyncCarriers:
        return AsyncCarriers(self)

    @cached_property
    def gateways(self) -> AsyncGateways:
        return AsyncGateways(self)

    @cached_property
    def phone_numbers(self) -> AsyncPhoneNumbers:
        return AsyncPhoneNumbers(self)

    @cached_property
    def applications(self) -> AsyncApplications:
        return AsyncApplications(self)

    @cached_property
    def speech_services(self) -> AsyncSpeechServices:
        return AsyncSpeechServices(self)

    # --- Call Control ---

    @cached_property
    def calls(self) -> AsyncCalls:
        return AsyncCalls(self)

    @cached_property
    def recent_calls(self) -> AsyncRecentCalls:
        return AsyncRecentCalls(self)
