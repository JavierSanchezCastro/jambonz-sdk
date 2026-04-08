import httpx


class JambonzError(Exception):
    pass


class JambonzAPIError(JambonzError):
    def __init__(self, message: str, status_code: int, response: httpx.Response | None = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class JambonzAuthError(JambonzAPIError):
    pass


class JambonzNotFoundError(JambonzAPIError):
    pass


class JambonzRateLimitError(JambonzAPIError):
    pass


class JambonzValidationError(JambonzAPIError):
    pass


def raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return

    message = f"{response.status_code}: {response.text}"

    error_map: dict[int, type[JambonzAPIError]] = {
        401: JambonzAuthError,
        403: JambonzAuthError,
        404: JambonzNotFoundError,
        422: JambonzValidationError,
        429: JambonzRateLimitError,
    }

    exc_class = error_map.get(response.status_code, JambonzAPIError)
    raise exc_class(message, response.status_code, response)
