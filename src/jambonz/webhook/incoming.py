"""Models for parsing incoming jambonz webhook payloads.

Usage with FastAPI:
    @app.post("/incoming-call")
    def handle_call(call: CallWebhook) -> JambonzResponse:
        print(f"Call from {call.from_} to {call.to}")
        return [Say(text="Hello"), Hangup()]

    @app.post("/gather-result")
    def handle_gather(result: GatherResult) -> JambonzResponse:
        print(f"User said: {result.speech.alternatives[0].transcript}")
        return [Say(text="Thanks"), Hangup()]
"""
from typing import Any

from pydantic import ConfigDict, Field

from jambonz.models._base import Sid, _JambonzModel
from jambonz.models.calls import CallStatus, Direction


# --- Call webhook (initial call event) ---

class SipRequest(_JambonzModel):
    raw: str | None = None
    method: str | None = None
    version: str | None = None
    uri: str | None = None
    headers: dict[str, Any] | None = None
    body: str | None = None
    payload: list[dict[str, Any]] | None = None


class CallWebhook(_JambonzModel):
    """Payload jambonz sends to your call_hook when a new call arrives.
    https://docs.jambonz.org/reference/webhooks/call-webhook"""
    call_sid: Sid | None = None
    call_id: str | None = None
    application_sid: Sid | None = None
    account_sid: Sid | None = None
    direction: Direction | None = None
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    caller_name: str | None = None
    sip_status: int | None = None
    sip_reason: str | None = None
    call_status: CallStatus | None = None
    sbc_callid: str | None = None
    originating_sip_ip: str | None = None
    originating_sip_trunk_name: str | None = None
    local_sip_address: str | None = None
    service_provider_sid: Sid | None = None
    sip: SipRequest | None = None
    env_vars: dict[str, Any] | None = None

    model_config = ConfigDict(populate_by_name=True)


# --- Call status webhook ---

class CallStatusEvent(_JambonzModel):
    """Payload jambonz sends to your call_status_hook."""
    call_sid: Sid | None = None
    call_id: str | None = None
    application_sid: Sid | None = None
    account_sid: Sid | None = None
    direction: Direction | None = None
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    call_status: CallStatus | None = None
    sip_status: int | None = None
    sip_reason: str | None = None
    duration: int | None = None

    model_config = ConfigDict(populate_by_name=True)


# --- Gather result ---

class SpeechAlternative(_JambonzModel):
    transcript: str = ""
    confidence: float = 0.0


class SpeechResult(_JambonzModel):
    language_code: str | None = None
    is_final: bool = True
    channel_tag: int | None = None
    alternatives: list[SpeechAlternative] = []
    vendor: dict[str, Any] | None = None


class GatherResult(_JambonzModel):
    """Payload jambonz sends to gather's actionHook."""
    reason: str | None = None  # "speechDetected", "dtmfDetected", "timeout", "error"
    speech: SpeechResult | None = None
    digits: str | None = None
    details: str | None = None  # error details

    @property
    def transcript(self) -> str | None:
        """Shortcut to get the best transcript."""
        if self.speech and self.speech.alternatives:
            return self.speech.alternatives[0].transcript
        return None


# --- Dial result ---

class DialResult(_JambonzModel):
    """Payload jambonz sends to dial's actionHook."""
    dial_call_sid: Sid | None = None
    dial_call_status: str | None = None  # "completed", "failed", "busy", "no-answer", "queued"
    dial_sip_status: int | None = None


# --- LLM result ---

class LLMResult(_JambonzModel):
    """Payload jambonz sends to llm's actionHook when session ends."""
    completion_reason: str | None = None
    error: dict[str, Any] | None = None


class ToolCall(_JambonzModel):
    """Payload jambonz sends to llm's toolHook."""
    name: str | None = None
    args: dict[str, Any] | None = None
    tool_call_id: str | None = None


class ToolResult(_JambonzModel):
    """Response to send back for a tool call."""
    type: str = "client_tool_result"
    tool_call_id: str | None = None
    result: Any = None
    is_error: bool = False
