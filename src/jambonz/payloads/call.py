"""Call webhooks: the call-info envelope, call_hook and call_status_hook."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import Field

from jambonz.payloads._base import Payload

CallDirection: TypeAlias = Literal["inbound", "outbound"]
CallStatusValue: TypeAlias = Literal[
    "trying",
    "ringing",
    "early-media",
    "in-progress",
    "queued",
    "failed",
    "busy",
    "no-answer",
    "completed",
]
CallTerminationBy: TypeAlias = Literal["caller", "jambonz"]


class CallInfo(Payload):
    """Fields jambonz includes in every call-related payload (``callInfo.toJSON()``).

    Status and verb-hook payloads are this envelope plus their own fields.

    The field set varies by hook (live): verb hooks carry ``fs_sip_address``,
    ``fs_public_ip`` and ``api_base_url``, while ``call_hook`` and waitHooks
    (e.g. conference's) carry ``local_sip_address``, ``public_ip``,
    ``has_recording`` and ``caller_name`` instead.

    Overloaded keys:

    * ``call_status`` is an int SIP code in the ``sip:refer`` eventHook, which is
      why that hook has its own model (``SipReferEvent``);
    * ``sip_status``/``sip_reason`` are the response to the in-dialog request in
      ``sip:request``'s actionHook (see ``SipRequestResult``), not the call's status;
    * ``duration`` is the conference age as a float in the conference statusHook.

    Sparse hooks that do NOT carry this envelope: the enqueue waitHook
    (``EnqueueWait``), the ``sip:refer`` eventHook (``SipReferEvent``) and the
    listen/conference websocket frames (``jambonz.payloads.listen``).
    """

    call_sid: str | None = None
    call_id: str | None = None
    account_sid: str | None = None
    application_sid: str | None = None
    parent_call_sid: str | None = None
    sbc_callid: str | None = None
    direction: CallDirection | str | None = None
    from_: str | None = Field(default=None, validation_alias="from", serialization_alias="from")
    to: str | None = None
    caller_name: str | None = None
    caller_id: str | None = None
    call_status: CallStatusValue | str | None = None
    sip_status: int | None = None
    sip_reason: str | None = None
    sip_reason_header: str | None = None
    trace_id: str | None = None
    originating_sip_ip: str | None = None
    originating_sip_trunk_name: str | None = None
    api_base_url: str | None = None
    fs_sip_address: str | None = None
    fs_public_ip: str | None = None
    duration: int | float | None = None
    """Seconds. Whole seconds for the call itself; conference statusHook events
    reuse the key for the conference's age with decimals (e.g. ``1.69``, seen live)."""
    call_termination_by: CallTerminationBy | str | None = None
    headers: dict[str, Any] | None = None
    customer_data: dict[str, Any] | None = Field(
        default=None, validation_alias="customerData", serialization_alias="customerData"
    )
    verb_id: str | None = None
    b3: str | None = None
    """B3 trace header (live on the conference statusHook; AsyncAPI ``session:new``)."""
    local_sip_address: str | None = None
    public_ip: str | None = None
    has_recording: bool | None = None


class SipInvite(Payload):
    """The SIP INVITE that started the call (POST call hooks only)."""

    method: str | None = None
    version: str | None = None
    uri: str | None = None
    headers: dict[str, Any] | None = None
    raw: str | None = None
    body: str | None = None
    payload: list[dict[str, Any]] | None = None


class CallDefaults(Payload):
    """Account/application speech defaults included in the call hook."""

    synthesizer: dict[str, Any] | None = None
    recognizer: dict[str, Any] | None = None


class CallWebhook(CallInfo):
    """Body of the application's ``call_hook`` (a new call)."""

    service_provider_sid: str | None = None
    defaults: CallDefaults | None = None
    env_vars: dict[str, Any] | None = None
    sip: SipInvite | None = None


class CallStatusEvent(CallInfo):
    """Body of the application's ``call_status_hook``.

    It is the call-info envelope itself; ``duration`` and ``call_termination_by``
    appear when the call completes (live). ``headers`` comes from the docs only
    and has not been seen live.
    """
