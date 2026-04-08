from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from jambonz._base import BaseClient, AsyncBaseClient

T = TypeVar("T", bound=BaseModel)


class SyncResource(Generic[T]):
    _model: type[T]
    _path: str  # e.g. "Accounts/{account_sid}/VoipCarriers" or "PhoneNumbers"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    @property
    def _base_path(self) -> str:
        return self._path.format(account_sid=self._client.account_sid)

    def list(self, **params: Any) -> list[T]:
        response = self._client.get(self._base_path, params=params)
        return [self._model.model_validate(item) for item in response.json()]

    def get(self, sid: str) -> T:
        response = self._client.get(f"{self._base_path}/{sid}")
        return self._model.model_validate(response.json())

    def create(self, **data: Any) -> T:
        response = self._client.post(self._base_path, json=data)
        return self._model.model_validate(response.json())

    def update(self, sid: str, **data: Any) -> T:
        response = self._client.put(f"{self._base_path}/{sid}", json=data)
        return self._model.model_validate(response.json())

    def delete(self, sid: str) -> None:
        self._client.delete(f"{self._base_path}/{sid}")


class AsyncResource(Generic[T]):
    _model: type[T]
    _path: str

    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    @property
    def _base_path(self) -> str:
        return self._path.format(account_sid=self._client.account_sid)

    async def list(self, **params: Any) -> list[T]:
        response = await self._client.get(self._base_path, params=params)
        return [self._model.model_validate(item) for item in response.json()]

    async def get(self, sid: str) -> T:
        response = await self._client.get(f"{self._base_path}/{sid}")
        return self._model.model_validate(response.json())

    async def create(self, **data: Any) -> T:
        response = await self._client.post(self._base_path, json=data)
        return self._model.model_validate(response.json())

    async def update(self, sid: str, **data: Any) -> T:
        response = await self._client.put(f"{self._base_path}/{sid}", json=data)
        return self._model.model_validate(response.json())

    async def delete(self, sid: str) -> None:
        await self._client.delete(f"{self._base_path}/{sid}")
