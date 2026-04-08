from typing import Any

from jambonz.models.calls import Call
from jambonz.resources._base import SyncResource, AsyncResource


class Calls(SyncResource[Call]):
    """Call control — active calls."""
    _model = Call
    _path = "Accounts/{account_sid}/Calls"

    def create(
        self,
        *,
        from_: str,
        to: dict[str, Any],
        application_sid: str | None = None,
        call_hook: str | None = None,
        call_status_hook: str | None = None,
        **kwargs: Any,
    ) -> Call:
        data: dict[str, Any] = {"from": from_, "to": to, **kwargs}
        if application_sid:
            data["application_sid"] = application_sid
        if call_hook:
            data["call_hook"] = call_hook
        if call_status_hook:
            data["call_status_hook"] = call_status_hook
        response = self._client.post(self._base_path, json=data)
        return Call.model_validate(response.json())


class AsyncCalls(AsyncResource[Call]):
    _model = Call
    _path = "Accounts/{account_sid}/Calls"

    async def create(
        self,
        *,
        from_: str,
        to: dict[str, Any],
        application_sid: str | None = None,
        call_hook: str | None = None,
        call_status_hook: str | None = None,
        **kwargs: Any,
    ) -> Call:
        data: dict[str, Any] = {"from": from_, "to": to, **kwargs}
        if application_sid:
            data["application_sid"] = application_sid
        if call_hook:
            data["call_hook"] = call_hook
        if call_status_hook:
            data["call_status_hook"] = call_status_hook
        response = await self._client.post(self._base_path, json=data)
        return Call.model_validate(response.json())
