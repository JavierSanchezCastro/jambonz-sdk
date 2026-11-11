"""The ``config`` verb: session-wide defaults and background features.

Field set: the union of ``specs.json`` (``config``), feature-server
``lib/tasks/config.js`` and the official SDK schema, minus ``transcribe``
(``TranscribeOptions`` is modelled with the transcribe batch; use
``extra_fields={"transcribe": {...}}`` until then).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

from pydantic import MISSING, StrictBool, StrictFloat, StrictInt, model_validator

from jambonz._wire import WireModel
from jambonz.types import Hook
from jambonz.verbs._base import VerbModel
from jambonz.verbs.components import (
    ActionHookDelayAction,
    Amd,
    BargeIn,
    FillerNoise,
    NoiseIsolation,
    RecordOptions,
    TurnTaking,
    Vad,
)
from jambonz.verbs.media import ListenOptions
from jambonz.verbs.shared import Recognizer, Synthesizer

__all__ = ["Config", "ResetTarget", "TtsStream"]

ResetTarget = Literal["recognizer", "synthesizer"]
"""What ``Config.reset`` can restore to the application defaults."""


class TtsStream(WireModel):
    """Turns background TTS streaming on (``enable=True``) or off (``enable=False``).

    When enabled without a ``synthesizer``, feature-server uses the one set by
    ``Config.synthesizer`` or the session defaults.
    """

    enable: StrictBool
    synthesizer: Synthesizer | MISSING = MISSING


class Config(VerbModel):
    """Change session defaults (speech, barge-in, recording, streaming, ...).

    Non-blocking: jambonz applies the settings and moves on to the next verb.
    Every field is optional. Some behaviours worth knowing:

    * ``synthesizer``/``recognizer`` still require ``vendor`` (``specs.json``
      requires it inside nested objects too); pass ``vendor="default"`` to keep
      the current vendor and change only e.g. the voice or language.
    * ``notify_events=False`` does not turn notifications off: feature-server
      only acts on a true value.
    * ``reset`` runs before the new ``synthesizer``/``recognizer`` is applied.
    * ``listen`` needs ``enable=True`` to start (``enable=False`` stops it); without
      ``enable`` jambonz does nothing and reports nothing (verified live).
    * No ``stream`` here, although it is ``listen``'s synonym in the ``stream``
      verb, ``dial`` and ``conference``: jambonz's validator accepts
      ``config.stream`` but ``config.js`` never reads it (the synonym, added in
      Jan 2025, never reached ``config``). Verified live: it neither starts nor
      stops a stream. Passing it is an error that points to ``listen``.
    * ``bargeIn``, ``record.action``, ``listen.url``, ``amd``, ``boostAudioSignal``
      and ``transcribe.enable`` need media, so they make jambonz answer the call.
    * ``early_media``, ``track_tts_playout``, ``noise_isolation`` and
      ``turn_taking`` (and ``barge_in.partial_result_hook``) are accepted by
      specs.json and the official schema, but feature-server 0.9.15 never reads
      them: jambonz takes them and does nothing. A newer feature-server (as on
      jambonz.cloud) may act on them; this is not yet checked end to end.
    """

    verb: Literal["config"] = "config"
    synthesizer: Synthesizer | MISSING = MISSING
    recognizer: Recognizer | MISSING = MISSING
    barge_in: BargeIn | MISSING = MISSING
    tts_stream: TtsStream | MISSING = MISSING
    record: RecordOptions | MISSING = MISSING
    listen: ListenOptions | MISSING = MISSING
    amd: Amd | MISSING = MISSING
    """Start answering machine detection in the background (see ``Amd``). An
    object with ``actionHook``: jambonz.cloud rejects the docs' ``amd: true``
    (verified live: the call fails with 480 and an ``invalid-app-payload`` alert)."""
    filler_noise: FillerNoise | MISSING = MISSING
    notify_events: StrictBool | MISSING = MISSING
    notify_stt_latency: StrictBool | MISSING = MISSING
    reset: ResetTarget | Sequence[ResetTarget] | MISSING = MISSING
    on_hold_music: str | MISSING = MISSING
    action_hook_delay_action: ActionHookDelayAction | MISSING = MISSING
    sip_request_within_dialog_hook: Hook | MISSING = MISSING
    boost_audio_signal: StrictInt | StrictFloat | str | MISSING = MISSING
    """Gain in dB: a number or a string such as ``"-6 dB"``. A string that does
    not match ``/([+-]?\\d+(\\.\\d+)?)\\s*db/i`` silently becomes 0."""
    vad: Vad | MISSING = MISSING
    refer_hook: Hook | MISSING = MISSING
    early_media: StrictBool | MISSING = MISSING
    auto_stream_tts: StrictBool | MISSING = MISSING
    disable_tts_cache: StrictBool | MISSING = MISSING
    track_tts_playout: StrictBool | MISSING = MISSING
    noise_isolation: NoiseIsolation | MISSING = MISSING
    turn_taking: TurnTaking | MISSING = MISSING

    @model_validator(mode="before")
    @classmethod
    def _reject_stream(cls, data: Any) -> Any:
        if isinstance(data, dict) and "stream" in data:
            raise ValueError(
                "config has no 'stream': jambonz ignores config.stream (the listen synonym "
                "was never implemented in config). Use listen=ListenOptions(enable=True, url=...)"
            )
        return data
