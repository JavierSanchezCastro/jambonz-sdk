from typing import Any

from jambonz.models.calls import RecentCall
from jambonz.resources._base import AsyncResource, SyncResource


class RecentCalls(SyncResource[RecentCall]):
    """Call history — paginated."""

    _model = RecentCall
    _path = "Accounts/{account_sid}/RecentCalls"

    def list(
        self, *, days: int = 7, page: int = 1, count: int = 25, **params: Any
    ) -> list[RecentCall]:
        params.update(days=days, page=page, count=count)
        response = self._client.get(self._base_path, params=params)
        data = response.json()
        return [self._model.model_validate(item) for item in data.get("data", data)]


class AsyncRecentCalls(AsyncResource[RecentCall]):
    _model = RecentCall
    _path = "Accounts/{account_sid}/RecentCalls"

    async def list(
        self, *, days: int = 7, page: int = 1, count: int = 25, **params: Any
    ) -> list[RecentCall]:
        params.update(days=days, page=page, count=count)
        response = await self._client.get(self._base_path, params=params)
        data = response.json()
        return [self._model.model_validate(item) for item in data.get("data", data)]
