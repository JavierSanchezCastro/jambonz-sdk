"""jambonz verbs: what a webhook answers with.

A webhook response is a plain list of verbs::

    def handle(call: CallWebhook) -> JambonzResponse:
        return [Say(text="Hello"), Hangup()]

FastAPI serializes it from the return annotation; elsewhere use ``to_json``.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated, Any, TypeAlias, get_args

from pydantic import Discriminator, TypeAdapter
from pydantic import Tag as _Tag  # `Tag` is the jambonz tag verb

from jambonz.verbs._base import Nested, VerbModel, literal_value
from jambonz.verbs.components import (
    ActionHookDelayAction,
    Amd,
    AmdTimers,
    BargeIn,
    FillerNoise,
    NoiseIsolation,
    NoiseIsolationAuth,
    RecordOptions,
    TurnTaking,
    Vad,
)
from jambonz.verbs.config import Config, TtsStream
from jambonz.verbs.control import Alert, Answer, Dtmf, Hangup, Leave, Pause, Redirect, Tag
from jambonz.verbs.dial import (
    Dial,
    DialFrom,
    DtmfCapture,
    PhoneTarget,
    SipTarget,
    Target,
    TeamsTarget,
    UserTarget,
)
from jambonz.verbs.gather import Gather
from jambonz.verbs.llm import LLM
from jambonz.verbs.media import (
    BidirectionalAudio,
    Dub,
    DubSay,
    Listen,
    ListenOptions,
    NestedListen,
    NestedStream,
    Stream,
)
from jambonz.verbs.play import Play
from jambonz.verbs.queues import Conference, ConferenceRecord, Dequeue, Enqueue
from jambonz.verbs.raw import RawVerb
from jambonz.verbs.say import Say
from jambonz.verbs.shared import Hint, Input, Recognizer, Synthesizer
from jambonz.verbs.sip import SipDecline, SipRefer, SipRequest

_RAW_TAG = "__raw__"
KNOWN_VERBS: frozenset[str]


def _verb_tag(value: Any) -> str:
    if isinstance(value, RawVerb):
        return _RAW_TAG
    name = value.get("verb") if isinstance(value, dict) else getattr(value, "verb", None)
    return name if isinstance(name, str) and name in KNOWN_VERBS else _RAW_TAG


Verb: TypeAlias = Annotated[
    (
        Annotated[Say, _Tag("say")]
        | Annotated[Play, _Tag("play")]
        | Annotated[Pause, _Tag("pause")]
        | Annotated[Hangup, _Tag("hangup")]
        | Annotated[Redirect, _Tag("redirect")]
        | Annotated[Answer, _Tag("answer")]
        | Annotated[Leave, _Tag("leave")]
        | Annotated[Alert, _Tag("alert")]
        | Annotated[Dtmf, _Tag("dtmf")]
        | Annotated[Tag, _Tag("tag")]
        | Annotated[SipDecline, _Tag("sip:decline")]
        | Annotated[SipRefer, _Tag("sip:refer")]
        | Annotated[SipRequest, _Tag("sip:request")]
        | Annotated[Gather, _Tag("gather")]
        | Annotated[Dial, _Tag("dial")]
        | Annotated[LLM, _Tag("llm")]
        | Annotated[Config, _Tag("config")]
        | Annotated[Listen, _Tag("listen")]
        | Annotated[Stream, _Tag("stream")]
        | Annotated[Dub, _Tag("dub")]
        | Annotated[Enqueue, _Tag("enqueue")]
        | Annotated[Dequeue, _Tag("dequeue")]
        | Annotated[Conference, _Tag("conference")]
        | Annotated[RawVerb, _Tag(_RAW_TAG)]
    ),
    Discriminator(_verb_tag),
]
"""Any verb: a strict model chosen by ``verb``, or ``RawVerb`` for unknown names."""


def _strict_members() -> tuple[type[VerbModel], ...]:
    """The strict verb classes in ``Verb``, checking each Tag against the model."""
    classes: list[type[VerbModel]] = []
    for member in get_args(get_args(Verb)[0]):
        cls, tag = get_args(member)
        if cls is RawVerb:
            continue
        if tag.tag != literal_value(cls):
            raise RuntimeError(f"Verb union tags {cls.__name__} as {tag.tag!r}")
        classes.append(cls)
    return tuple(classes)


VERB_CLASSES: tuple[type[VerbModel], ...] = _strict_members()
"""Every strict verb model in the ``Verb`` union."""

KNOWN_VERBS = frozenset(literal_value(cls) for cls in VERB_CLASSES)
"""Wire names parsed into a strict model; any other name parses as ``RawVerb``."""

JambonzResponse: TypeAlias = Sequence[Verb]
"""What a call/action hook returns: a sequence (usually a list) of verbs."""

_RESPONSE_ADAPTER: TypeAdapter[Sequence[Verb]] = TypeAdapter(JambonzResponse)


def to_json(verbs: JambonzResponse) -> bytes:
    """Serialize a verb list to the JSON body jambonz expects (Flask, Django, ...)."""
    return _RESPONSE_ADAPTER.dump_json(verbs)


__all__ = [
    "KNOWN_VERBS",
    "LLM",
    "VERB_CLASSES",
    "ActionHookDelayAction",
    "Alert",
    "Amd",
    "AmdTimers",
    "Answer",
    "BargeIn",
    "BidirectionalAudio",
    "Conference",
    "ConferenceRecord",
    "Config",
    "Dequeue",
    "Dial",
    "DialFrom",
    "Dtmf",
    "DtmfCapture",
    "Dub",
    "DubSay",
    "Enqueue",
    "FillerNoise",
    "Gather",
    "Hangup",
    "Hint",
    "Input",
    "JambonzResponse",
    "Leave",
    "Listen",
    "ListenOptions",
    "Nested",
    "NestedListen",
    "NestedStream",
    "NoiseIsolation",
    "NoiseIsolationAuth",
    "Pause",
    "PhoneTarget",
    "Play",
    "RawVerb",
    "Recognizer",
    "RecordOptions",
    "Redirect",
    "Say",
    "SipDecline",
    "SipRefer",
    "SipRequest",
    "SipTarget",
    "Stream",
    "Synthesizer",
    "Tag",
    "Target",
    "TeamsTarget",
    "TtsStream",
    "TurnTaking",
    "UserTarget",
    "Vad",
    "Verb",
    "VerbModel",
    "to_json",
]
