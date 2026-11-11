"""Payloads of ``transfer``'s actionHook."""

from __future__ import annotations

from typing import Literal, TypeAlias

from jambonz.payloads.call import CallInfo

TransferOutcome: TypeAlias = Literal["bridged", "returned", "voicemail", "failed"]
TransferReason: TypeAlias = Literal[
    "completed", "no-answer", "busy", "declined", "caller-abandoned", "error"
]


class TransferResult(CallInfo):
    """Body of ``transfer``'s actionHook. Source: official schema/docs only (not live yet).

    ``'voicemail'`` is sent only to ``disposition.voicemailUrl``. The envelope's
    ``sip_status`` carries the transfer dial's final SIP status, not the
    caller's. The transfer eventHook (``event_type``, camelCase
    ``callerPresent``) is not modelled.
    """

    transfer_result: TransferOutcome | str | None = None
    transfer_reason: TransferReason | str | None = None
    dial_call_sid: str | None = None
