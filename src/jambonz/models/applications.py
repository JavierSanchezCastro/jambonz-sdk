from typing import Any

from jambonz.models._base import Sid, Webhook, _JambonzModel


class Application(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/applications/list-applications"""
    name: str = ""
    application_sid: Sid | None = None
    account_sid: Sid | None = None
    call_hook: Webhook | str | None = None
    call_status_hook: Webhook | str | None = None
    messaging_hook: Webhook | str | None = None
    speech_synthesis_vendor: str | None = None
    speech_synthesis_voice: str | None = None
    speech_recognizer_vendor: str | None = None
    speech_recognizer_language: str | None = None
    env_vars: dict[str, Any] | None = None
    record_all_calls: bool = False
