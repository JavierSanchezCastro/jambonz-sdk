"""Payloads of ``gather``'s hooks: the actionHook result and partial transcripts."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from jambonz.payloads._base import Payload
from jambonz.payloads.call import CallInfo

GatherReason: TypeAlias = Literal[
    "speechDetected", "dtmfDetected", "stt-low-confidence", "timeout", "error"
]


class SpeechAlternative(Payload):
    transcript: str | None = None
    confidence: float | None = None


class SpeechTranscript(Payload):
    is_final: bool | None = None
    language_code: str | None = None
    channel_tag: int | None = None
    alternatives: list[SpeechAlternative] | None = None


class SpeechVendor(Payload):
    name: str | None = None
    evt: Any = None


class SpeechResult(Payload):
    """The ``speech`` object of a gather result.

    The canonical shape has ``alternatives`` directly under ``speech`` (official
    ``gather.schema.json`` and feature-server ``transcription-utils.js``, which
    normalizes every STT vendor to it). The docs/verb:hook examples nest them in
    ``transcripts[]``; that shape is tolerated too, and ``transcript`` reads either.
    """

    is_final: bool | None = None
    language_code: str | None = None
    channel_tag: int | None = None
    alternatives: list[SpeechAlternative] | None = None
    transcripts: list[SpeechTranscript] | None = None
    vendor: SpeechVendor | None = None

    @property
    def transcript(self) -> str | None:
        """Best transcript, or ``None`` if there is none."""
        for alternatives in (self.alternatives, *(t.alternatives for t in self.transcripts or [])):
            if alternatives:
                return alternatives[0].transcript
        return None


class GatherResult(CallInfo):
    """Body of ``gather``'s actionHook (live, official schema, docs).

    Also covers the ``config.bargeIn`` actionHook (live: ``dtmfDetected`` plus
    ``digits``). Only ``dtmfDetected`` has been captured live so far;
    ``speechDetected``, ``timeout``, ``error`` and ``stt-low-confidence`` come from
    the official schema and docs.
    """

    reason: GatherReason | str | None = None
    speech: SpeechResult | None = None
    digits: str | None = None
    details: str | dict[str, Any] | None = None

    @property
    def transcript(self) -> str | None:
        """Shortcut to the best transcript."""
        return self.speech.transcript if self.speech else None


class GatherPartialResult(CallInfo):
    """Body of ``gather``'s partialResultHook: interim transcripts (``speech.is_final``
    is false); jambonz ignores the response.

    Source: official ``gather-partial`` schema (not captured live yet; needs STT).
    """

    speech: SpeechResult | None = None

    @property
    def transcript(self) -> str | None:
        """Shortcut to the best interim transcript."""
        return self.speech.transcript if self.speech else None
