"""Components shared by several verbs."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import Any, Literal

from pydantic import MISSING, StrictBool, StrictFloat, StrictInt

from jambonz._wire import WireModel


class Input(str, Enum):
    """Values for ``Gather.input`` and ``BargeIn.input``.

    Plain strings ``"digits"``/``"speech"`` work too.
    """

    DIGITS = "digits"
    SPEECH = "speech"


class Synthesizer(WireModel):
    """Text-to-speech settings. Only ``vendor`` is required.

    ``vendor`` is an open string (``"default"``, ``"google"``, ``"custom:<name>"``...).
    Some vendors need ``voice`` in practice (e.g. Deepgram), but jambonz does not
    require it.
    """

    vendor: str
    label: str | MISSING = MISSING
    language: str | MISSING = MISSING
    voice: str | dict[str, Any] | MISSING = MISSING
    engine: Literal["standard", "neural", "generative", "long-form"] | MISSING = MISSING
    gender: Literal["MALE", "FEMALE", "NEUTRAL"] | MISSING = MISSING
    options: dict[str, Any] | MISSING = MISSING
    fallback_vendor: str | MISSING = MISSING
    fallback_label: str | MISSING = MISSING
    fallback_language: str | MISSING = MISSING
    fallback_voice: str | dict[str, Any] | MISSING = MISSING


class Hint(WireModel):
    """A recognizer hint with its own boost."""

    phrase: str
    boost: StrictInt | StrictFloat | MISSING = MISSING


class Recognizer(WireModel):
    """Speech-to-text settings. Only ``vendor`` is required.

    Partial model: vendor-specific option blocks (``deepgramOptions``, ...) and the
    less common fields are not modelled yet; use ``extra_fields`` for them.
    """

    vendor: str
    label: str | MISSING = MISSING
    language: str | MISSING = MISSING
    fallback_vendor: str | MISSING = MISSING
    fallback_label: str | MISSING = MISSING
    fallback_language: str | MISSING = MISSING
    alt_languages: Sequence[str] | MISSING = MISSING
    hints: Sequence[str | Hint] | MISSING = MISSING
    hints_boost: StrictInt | StrictFloat | MISSING = MISSING
    model: str | MISSING = MISSING
    interim: StrictBool | MISSING = MISSING
    punctuation: StrictBool | MISSING = MISSING
    profanity_filter: StrictBool | MISSING = MISSING
    single_utterance: StrictBool | MISSING = MISSING
    min_confidence: StrictInt | StrictFloat | MISSING = MISSING
    asr_timeout: StrictInt | StrictFloat | MISSING = MISSING
    asr_dtmf_termination_digit: str | MISSING = MISSING
    initial_speech_timeout_ms: StrictInt | StrictFloat | MISSING = MISSING
    fast_recognition_timeout: StrictInt | StrictFloat | MISSING = MISSING
