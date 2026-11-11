"""SIP verbs: sip:decline, sip:refer, sip:request."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import MISSING, Field, StrictInt

from jambonz.types import Hook
from jambonz.verbs._base import VerbModel


class SipDecline(VerbModel):
    """Reject an incoming call with a SIP final response (400-699)."""

    verb: Literal["sip:decline"] = "sip:decline"
    status: Annotated[StrictInt, Field(ge=400, le=699)]
    reason: str | MISSING = MISSING
    headers: dict[str, str | StrictInt] | MISSING = MISSING


class SipRefer(VerbModel):
    """Transfer the caller elsewhere with a SIP REFER (blind transfer)."""

    verb: Literal["sip:refer"] = "sip:refer"
    refer_to: str
    referred_by: str | MISSING = MISSING
    referred_by_display_name: str | MISSING = MISSING
    headers: dict[str, str] | MISSING = MISSING
    action_hook: Hook | MISSING = MISSING
    event_hook: Hook | MISSING = MISSING


class SipRequest(VerbModel):
    """Send an in-dialog SIP INFO, MESSAGE or NOTIFY to the caller."""

    verb: Literal["sip:request"] = "sip:request"
    method: Literal["INFO", "MESSAGE", "NOTIFY"]
    body: str | MISSING = MISSING
    headers: dict[str, str] | MISSING = MISSING
    action_hook: Hook | MISSING = MISSING
