"""Payloads of ``amd``'s actionHook (``config.amd`` / ``dial.amd``)."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from jambonz.payloads.call import CallInfo

AmdType: TypeAlias = Literal[
    "amd_human_detected",
    "amd_machine_detected",
    "amd_no_speech_detected",
    "amd_decision_timeout",
    "amd_machine_stopped_speaking",
    "amd_tone_detected",
    "amd_tone_timeout",
    "amd_error",
    "amd_stopped",
]


class AmdEvent(CallInfo):
    """Body of the ``amd`` actionHook (``config.amd`` or ``dial.amd``). Source: live.

    jambonz can send several events per call (live: ``amd_no_speech_detected``
    then ``amd_stopped``). The discriminator key is ``type`` (live, official
    schema); the ``event``/``amd_type`` keys in dial.md's "amd.hook properties"
    are stale and never sent (they would land in ``model_extra``).
    ``frequency``/``variance`` accompany tone detection (official schema only);
    ``transcript`` and ``error`` come from the AMD guide only.
    """

    type: AmdType | str
    reason: str | None = None
    """Why the decision was made, e.g. ``'hint'``, ``'short greeting'`` (official; guide)."""
    greeting: str | None = None
    hint: str | None = None
    language: str | None = None
    transcript: str | None = None
    """Recognised greeting on ``amd_machine_detected`` (AMD guide only)."""
    error: Any = None
    """Error detail on ``amd_error`` (AMD guide only)."""
    frequency: float | None = None
    """Tone frequency in Hz on tone detection (official schema only)."""
    variance: float | None = None
