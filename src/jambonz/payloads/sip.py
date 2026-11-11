"""Payloads of ``sip:request``/``sip:refer`` hooks."""

from __future__ import annotations

from typing import Literal, TypeAlias

from jambonz.payloads._base import Payload
from jambonz.payloads.call import CallInfo

SipRequestOutcome: TypeAlias = Literal["success", "failed"]
SipReferEventType: TypeAlias = Literal["transfer-status"]


class SipRequestResult(CallInfo):
    """Body of ``sip:request``'s actionHook (live, official schema).

    Overloaded envelope keys: ``sip_status``/``sip_reason`` are the response to
    the in-dialog request, not the call's status. Live, a 488 came back with
    ``result='success'`` and ``sip_reason='OK'``, so ``sip_status`` is the
    reliable field. ``err`` is set on failure (official/docs).
    """

    result: SipRequestOutcome | str
    err: str | None = None


class SipReferResult(CallInfo):
    """Body of ``sip:refer``'s actionHook (live, official schema).

    ``refer_status`` is the SIP response to the REFER (live 202);
    ``final_referred_call_status`` is the referred call's final SIP status, from
    the NOTIFY (live 200). Docs say ``referStatus``; the wire is snake_case.
    """

    refer_status: int
    final_referred_call_status: int | None = None


class SipReferEvent(Payload):
    """Body of ``sip:refer``'s eventHook, one per NOTIFY (live, official schema).

    Sparse: exactly these two keys live, no call envelope (so not a
    ``CallInfo``). ``call_status`` is the SIP status code from the NOTIFY
    sipfrag (live int 100, 200; docs example string ``'180'``), NOT a
    ``CallStatusValue`` value; ``CallInfo`` would reject it.
    """

    event: SipReferEventType | str
    call_status: int | str
