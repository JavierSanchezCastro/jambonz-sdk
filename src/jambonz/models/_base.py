from uuid import UUID

from pydantic import BaseModel, ConfigDict

Sid = UUID


class _JambonzModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class Webhook(_JambonzModel):
    webhook_sid: Sid | None = None
    url: str | None = None
    method: str = "POST"
    username: str | None = None
    password: str | None = None
