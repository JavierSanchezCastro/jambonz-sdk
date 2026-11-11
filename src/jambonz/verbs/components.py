"""Nested settings objects shared by ``config``, ``dial`` and ``gather``.

None of these is a verb: they are plain components (``WireModel``). Field names
follow the union of the jambonz docs, ``@jambonz/verb-specifications``
(``specs.json``) and the official SDK schemas; where they disagree the class
docstring says so.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cache
from typing import TYPE_CHECKING, Annotated, Any, Literal, TypeAlias

from pydantic import (
    MISSING,
    BeforeValidator,
    Field,
    SerializeAsAny,
    StrictBool,
    StrictFloat,
    StrictInt,
    TypeAdapter,
    WithJsonSchema,
)

from jambonz._wire import WireModel
from jambonz.types import Hook
from jambonz.verbs._base import VerbModel
from jambonz.verbs.play import Play
from jambonz.verbs.raw import RawVerb
from jambonz.verbs.say import Say
from jambonz.verbs.shared import Input, Recognizer

if TYPE_CHECKING:
    from jambonz.verbs import Verb as _GiveUpVerb

__all__ = [
    "ActionHookDelayAction",
    "Amd",
    "AmdTimers",
    "BargeIn",
    "FillerNoise",
    "NoiseIsolation",
    "NoiseIsolationAuth",
    "RecordOptions",
    "TurnTaking",
    "Vad",
]

Number: TypeAlias = StrictInt | StrictFloat
_Unit: TypeAlias = (
    Annotated[StrictInt, Field(ge=0, le=1)] | Annotated[StrictFloat, Field(ge=0, le=1)]
)
"""A number between 0 and 1 (thresholds)."""
_Percent: TypeAlias = (
    Annotated[StrictInt, Field(ge=0, le=100)] | Annotated[StrictFloat, Field(ge=0, le=100)]
)


# --- actionHookDelayAction ---------------------------------------------------------


@cache
def _verb_adapter() -> TypeAdapter[Any]:
    # Imported on first use: ``jambonz.verbs`` imports the verbs that import this
    # module, so a top-level import would be a cycle.
    from jambonz.verbs import Verb

    return TypeAdapter(Verb)


def _parse_verb(value: Any) -> Any:
    if isinstance(value, dict):
        return _verb_adapter().validate_python(value)
    if isinstance(value, VerbModel) and "verb" not in type(value).model_fields:
        # The bare base class (or a private intermediate) has no wire name, so it
        # would be sent without "verb" and jambonz could not run it.
        raise ValueError(f"{type(value).__name__} is not a concrete verb (it has no 'verb')")
    return value


def _parse_verb_dicts(value: Any) -> Any:
    """Turn wire dicts into verb models through the ``Verb`` union (models pass as is)."""
    if isinstance(value, list | tuple):
        return [_parse_verb(v) for v in value]
    return value


AnyVerb: TypeAlias = Annotated[
    SerializeAsAny[VerbModel] | RawVerb,
    WithJsonSchema(
        {"type": "object", "properties": {"verb": {"type": "string"}}, "required": ["verb"]}
    ),
]
"""Any verb, serialized with its ``"verb"`` key (whatever its concrete class)."""

if not TYPE_CHECKING:
    # Type checkers see the closed ``Verb`` union (so a bare ``VerbModel()`` is a
    # type error); at runtime ``AnyVerb`` keeps subclasses of the verbs working.
    _GiveUpVerb = AnyVerb


class ActionHookDelayAction(WireModel):
    """What to play while an actionHook is slow to answer, and what to do if it never does.

    ``actions`` run (in turn, up to ``retries`` extra times) once
    ``no_response_timeout`` seconds pass without a response; feature-server only
    accepts ``say`` and ``play`` there. ``give_up_actions`` (any verbs) replace the
    application if no response arrives within ``no_response_give_up_timeout``
    seconds. Over HTTP the 10 s request timeout caps the give-up wait.

    Both lists hold top-level verbs: feature-server reads their ``"verb"`` key, so
    unlike other nested verbs they keep it on the wire.

    feature-server also accepts ``enable`` for ``enabled``; specs.json and the docs
    only have ``enabled``, so that is the one modelled.
    """

    enabled: StrictBool | MISSING = MISSING
    no_response_timeout: Number | MISSING = MISSING
    no_response_give_up_timeout: Number | MISSING = MISSING
    retries: StrictInt | MISSING = MISSING
    actions: Sequence[Annotated[Say | Play, Field(discriminator="verb")]] | MISSING = MISSING
    give_up_actions: Annotated[
        Sequence[_GiveUpVerb] | MISSING, BeforeValidator(_parse_verb_dicts)
    ] = MISSING


# --- amd ---------------------------------------------------------------------------


class AmdTimers(WireModel):
    """AMD detection windows, in milliseconds. jambonz defaults: 5000, 15000, 20000, 2000."""

    no_speech_timeout_ms: Number | MISSING = MISSING
    decision_timeout_ms: Number | MISSING = MISSING
    tone_timeout_ms: Number | MISSING = MISSING
    greeting_completion_timeout_ms: Number | MISSING = MISSING


class Amd(WireModel):
    """Answering machine detection; results are posted to ``action_hook``.

    AMD runs in the background: after ``config`` with ``amd``, keep the call alive
    (e.g. with ``pause``) or the application ends. jambonz posts one or more events
    to ``action_hook`` (``{"type": "amd_human_detected", ...}``, ``amd_machine_detected``,
    ``amd_no_speech_detected``, ``amd_tone_detected``, ``amd_stopped``...); the hook
    may answer with new verbs.

    Pass a ``recognizer`` whose vendor has credentials in the account: AMD
    transcribes the greeting, and without one it uses the application default.
    Verified live: if that vendor has no credentials, AMD fails silently (no events;
    only ``Error calling startAmd`` in the call log and a ``no-stt`` alert). With
    Deepgram and a 440 Hz tone it sent ``amd_no_speech_detected`` (~5 s) then
    ``amd_stopped``.
    """

    action_hook: Hook
    threshold_word_count: StrictInt | MISSING = MISSING
    digit_count: StrictInt | MISSING = MISSING
    timers: AmdTimers | MISSING = MISSING
    recognizer: Recognizer | MISSING = MISSING


# --- bargeIn -----------------------------------------------------------------------


class BargeIn(WireModel):
    """Session-wide barge-in (``config.bargeIn``): let callers interrupt prompts.

    When enabled, jambonz runs a background gather with these settings on every
    prompt; results go to ``action_hook``. ``sticky`` keeps it enabled across verbs.
    The docs mark ``input`` as required; specs.json does not (jambonz then listens
    for speech only).

    Verified on jambonz.cloud with digits: the first digit stops the playing verb
    and jambonz goes straight on to the next one; ``action_hook`` is called only
    when the collection completes (e.g. ``finish_on_key``), and its response
    replaces the remaining verbs. If the call ends first (say the next verb is
    ``hangup``), the hook is never called.

    ``partial_result_hook`` is accepted by specs.json and the official schema, but
    feature-server 0.9.15 does not act on it: ``config.js`` copies only a fixed key
    list into the background gather and this key is not in it. That list also
    includes ``bargein``, which specs.json does not allow, so it is not modelled.
    """

    enable: StrictBool
    sticky: StrictBool | MISSING = MISSING
    action_hook: Hook | MISSING = MISSING
    partial_result_hook: Hook | MISSING = MISSING
    input: Sequence[Input | Literal["digits", "speech"]] | MISSING = MISSING
    finish_on_key: str | MISSING = MISSING
    num_digits: StrictInt | MISSING = MISSING
    min_digits: StrictInt | MISSING = MISSING
    max_digits: StrictInt | MISSING = MISSING
    inter_digit_timeout: Number | MISSING = MISSING
    dtmf_bargein: StrictBool | MISSING = MISSING
    min_bargein_word_count: StrictInt | MISSING = MISSING


# --- vad, noise isolation, turn taking ---------------------------------------------


class Vad(WireModel):
    """Voice activity detection for the session.

    ``mode`` (0-3, aggressiveness) applies to the ``webrtc`` vendor; ``threshold``
    (0-1) and ``speech_pad_ms`` to ``silero``. ``strategy`` is an open string
    (feature-server's default is ``"one-shot"``). feature-server fills every unset
    field with its own default once ``vad`` is given.
    """

    enable: StrictBool | MISSING = MISSING
    voice_ms: Number | MISSING = MISSING
    silence_ms: Number | MISSING = MISSING
    strategy: str | MISSING = MISSING
    mode: Annotated[StrictInt, Field(ge=0, le=3)] | MISSING = MISSING
    vendor: Literal["webrtc", "silero"] | MISSING = MISSING
    threshold: _Unit | MISSING = MISSING
    speech_pad_ms: Number | MISSING = MISSING


class NoiseIsolationAuth(WireModel):
    """Inline credentials for a noise-isolation vendor that needs them (kugelaudio)."""

    api_key: str | MISSING = MISSING
    api_uri: str | MISSING = MISSING
    """Vendor API host, e.g. ``api.eu.kugelaudio.com``."""


class NoiseIsolation(WireModel):
    """Background-noise removal on the call audio.

    ``vendor`` is an open string (``krisp``, ``rnnoise``, ``kugelaudio`` so far).
    ``level`` is 0-100. ``direction`` picks the inbound (``read``, the default per
    the docs) or outbound (``write``) audio. ``label``, ``auth`` and ``direction``
    come from the docs and the official schema; specs.json's ``noiseIsolation``
    lacks them, so jambonz's strict validator would reject them on the ``config``
    verb.

    feature-server 0.9.15 does not read ``config.noiseIsolation`` at all (jambonz
    accepts it and does nothing); a newer feature-server may. Not yet checked on
    jambonz.cloud.
    """

    enable: StrictBool | MISSING = MISSING
    vendor: str | MISSING = MISSING
    level: _Percent | MISSING = MISSING
    model: str | MISSING = MISSING
    label: str | MISSING = MISSING
    auth: NoiseIsolationAuth | MISSING = MISSING
    direction: Literal["read", "write"] | MISSING = MISSING


class TurnTaking(WireModel):
    """End-of-turn detection for voice agents. ``vendor`` is an open string (``krisp``).

    ``threshold`` is a 0-1 confidence (jambonz default 0.5, per the docs).

    feature-server 0.9.15 does not read ``config.turnTaking`` (jambonz accepts it
    and does nothing); a newer feature-server may. Not yet checked on jambonz.cloud.
    """

    enable: StrictBool | MISSING = MISSING
    vendor: str | MISSING = MISSING
    threshold: _Unit | MISSING = MISSING
    model: str | MISSING = MISSING


# --- filler noise ------------------------------------------------------------------


class FillerNoise(WireModel):
    """Background noise while waiting for an actionHook (``config`` and ``gather``).

    Deprecated in jambonz; kept for completeness.
    """

    enable: StrictBool
    url: str | MISSING = MISSING
    start_delay_secs: StrictInt | StrictFloat | MISSING = MISSING


# --- record ------------------------------------------------------------------------


class RecordOptions(WireModel):
    """Start, stop, pause or resume call recording (``config.record``).

    ``type`` is ``siprec`` (jambonz's default: stream to the SIPREC server at
    ``siprec_server_url``) or ``cloud`` (the account's recording storage).
    ``headers`` go to the SIPREC server as a JSON body. ``silence`` (cloud: record
    silence while paused) is read by feature-server and documented for REST call
    control, but is not in specs.json, so the strict validator rejects it on the
    ``config`` verb.
    """

    action: Literal[
        "startCallRecording", "stopCallRecording", "pauseCallRecording", "resumeCallRecording"
    ]
    type: Literal["siprec", "cloud"] | MISSING = MISSING
    recording_id: str | MISSING = Field(
        default=MISSING, validation_alias="recordingID", serialization_alias="recordingID"
    )
    siprec_server_url: str | Sequence[str] | MISSING = Field(
        default=MISSING, validation_alias="siprecServerURL", serialization_alias="siprecServerURL"
    )
    headers: dict[str, Any] | MISSING = MISSING
    silence: StrictBool | MISSING = MISSING
