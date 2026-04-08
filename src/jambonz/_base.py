from __future__ import annotations

import time
from typing import Any, Callable, Self

import httpx

from jambonz.config import JambonzSettings
from jambonz.exceptions import JambonzRateLimitError, raise_for_status


class BaseClient:
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
        kwargs: dict = {}
        if account_sid is not None:
            kwargs["account_sid"] = account_sid
        if api_key is not None:
            kwargs["api_key"] = api_key
        if base_url is not None:
            kwargs["base_url"] = base_url
        if timeout is not None:
            kwargs["timeout"] = timeout
        if max_retries is not None:
            kwargs["max_retries"] = max_retries
        settings = JambonzSettings(**kwargs)

        self.account_sid = settings.account_sid
        self.base_url = settings.base_url.rstrip("/")
        self.max_retries = settings.max_retries
        self.on_request = on_request
        self.on_response = on_response

        self._http = httpx.Client(
            base_url=f"{self.base_url}/v1/",
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
            },
            timeout=settings.timeout,
            event_hooks={
                "request": [on_request] if on_request else [],
                "response": [on_response] if on_response else [],
            },
        )

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        from jambonz.exceptions import JambonzAPIError

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self._http.request(method, path, **kwargs)
                raise_for_status(response)
                return response
            except JambonzRateLimitError as e:
                last_exc = e
                if attempt < self.max_retries:
                    retry_after = float(e.response.headers.get("Retry-After", 2 ** attempt)) if e.response else 2 ** attempt
                    time.sleep(retry_after)
                else:
                    raise
            except JambonzAPIError as e:
                if e.status_code >= 500 and attempt < self.max_retries:
                    last_exc = e
                    time.sleep(2 ** attempt)
                else:
                    raise
        raise last_exc  # type: ignore[misc]

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncBaseClient:
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
        kwargs: dict = {}
        if account_sid is not None:
            kwargs["account_sid"] = account_sid
        if api_key is not None:
            kwargs["api_key"] = api_key
        if base_url is not None:
            kwargs["base_url"] = base_url
        if timeout is not None:
            kwargs["timeout"] = timeout
        if max_retries is not None:
            kwargs["max_retries"] = max_retries
        settings = JambonzSettings(**kwargs)

        self.account_sid = settings.account_sid
        self.base_url = settings.base_url.rstrip("/")
        self.max_retries = settings.max_retries

        self._http = httpx.AsyncClient(
            base_url=f"{self.base_url}/v1/",
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
            },
            timeout=settings.timeout,
            event_hooks={
                "request": [on_request] if on_request else [],
                "response": [on_response] if on_response else [],
            },
        )

    async def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        import asyncio

        from jambonz.exceptions import JambonzAPIError

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._http.request(method, path, **kwargs)
                raise_for_status(response)
                return response
            except JambonzRateLimitError as e:
                last_exc = e
                if attempt < self.max_retries:
                    retry_after = float(e.response.headers.get("Retry-After", 2 ** attempt)) if e.response else 2 ** attempt
                    await asyncio.sleep(retry_after)
                else:
                    raise
            except JambonzAPIError as e:
                if e.status_code >= 500 and attempt < self.max_retries:
                    last_exc = e
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
        raise last_exc  # type: ignore[misc]

    async def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
