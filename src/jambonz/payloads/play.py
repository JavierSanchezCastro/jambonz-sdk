"""Payloads of ``play``'s actionHook."""

from __future__ import annotations

from typing import Literal, TypeAlias

from jambonz.payloads.call import CallInfo

PlayReason: TypeAlias = Literal["playCompleted", "playFailed"]
PlayStatus: TypeAlias = Literal["fail"]


class PlayResult(CallInfo):
    """Body of ``play``'s actionHook. Source: official schema/docs (no live capture yet).

    ``status`` ``'fail'`` accompanies ``reason`` ``'playFailed'``. ``reason`` is
    required by the official schema but kept optional until seen live.
    """

    reason: PlayReason | str | None = None
    playback_seconds: int | None = None
    playback_milliseconds: int | None = None
    playback_last_offset_pos: int | str | None = None
    """Offset position in samples where playback stopped (official types it as
    a string, docs describe a number)."""
    status: PlayStatus | str | None = None
