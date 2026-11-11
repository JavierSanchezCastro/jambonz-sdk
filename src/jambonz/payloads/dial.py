"""Payloads of ``dial``'s hooks."""

from __future__ import annotations

from pydantic import Field

from jambonz.payloads._base import Payload
from jambonz.payloads.call import CallInfo, CallStatusValue


class DialResult(CallInfo):
    """Body of ``dial``'s actionHook (live, official schema).

    ``dial_call_status`` reuses the open ``CallStatusValue`` (official enum: completed,
    failed, busy, no-answer, trying, ringing, early-media, in-progress; docs add
    queued). jambonz does not send ``dial_call_duration`` (not in the official
    schema, not live); call duration is not reported here.
    """

    dial_call_sid: str | None = None
    dial_call_status: CallStatusValue | str | None = None
    dial_sip_status: int | None = None
    dial_sbc_callid: str | None = None


class HoldDetail(Payload):
    """From/To headers of the hold re-INVITE (official dial-hold; docs dial.md)."""

    from_: str | None = Field(default=None, validation_alias="from", serialization_alias="from")
    to: str | None = None


class ReferDetails(Payload):
    """Details of a REFER received on the dialed leg (official dial-refer).

    Custom ``X-*`` headers of the REFER land in ``model_extra``.
    """

    sip_refer_to: str | None = None
    refer_to_user: str | None = None
    sip_referred_by: str | None = None
    referred_by_user: str | None = None
    sip_user_agent: str | None = None
    referring_call_sid: str | None = None
    referred_call_sid: str | None = None


class DialDtmfEvent(CallInfo):
    """Body of ``dial``'s dtmfHook (official schema only, not captured live).

    Fires when a ``dtmfCapture`` pattern matches; notification only, the
    response is ignored. ``dtmf`` is official-required but optional here until
    seen live.
    """

    dtmf: str | None = None


class DialHoldEvent(CallInfo):
    """Body of ``dial``'s onHoldHook (official schema, docs; not captured live).

    The response may contain only ``play``/``say``/``pause``.
    """

    hold_detail: HoldDetail | None = None


class DialReferEvent(CallInfo):
    """Body of ``dial``'s referHook on the dialed leg (official schema; not live).

    Reply with HTTP 200 and an empty body, not verbs.
    """

    refer_details: ReferDetails | None = None
