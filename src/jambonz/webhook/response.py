from typing import Any

from pydantic import RootModel, model_serializer

from jambonz.webhook.verbs import Verb


class JambonzResponse(RootModel[list[Verb]]):
    """A list of jambonz verbs to return as a webhook response.

    Usage:
        # FastAPI — type hint, return raw list
        @app.post("/call")
        def handle() -> JambonzResponse:
            return [Say(text="Hello"), Hangup()]

        # Flask / Django — construct and serialize
        response = JambonzResponse([Say(text="Hello"), Hangup()])
        response.model_dump()       # → list[dict]
        response.model_dump_json()  # → str
    """

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> list[dict]:
        return [
            v.model_dump(mode="json", by_alias=True, exclude_none=True)
            for v in self.root
        ]
