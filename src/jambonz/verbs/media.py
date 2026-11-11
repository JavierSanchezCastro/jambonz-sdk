"""Media verbs: ``listen`` (and its alias ``stream``) and ``dub``.

Nesting, as feature-server reads it:

* ``dial.listen`` / ``dial.stream`` and ``conference.listen`` hold a full listen
  verb without ``verb`` (specs.json types them ``#listen``; dial passes the object
  to ``makeTask({listen: ...})``). Type them ``NestedListen`` / ``NestedStream``
  (a ``Listen`` or a ``Stream``, sent without ``verb``): ``url`` is required there
  too and there is no ``enable``.
* ``config.listen`` / ``config.stream`` are a different shape (specs.json
  ``#listenOptions``): ``enable`` is required, ``url`` is optional and the
  verb-only fields (``actionHook``, ``finishOnKey``, ``transcribe``, ...) are not
  accepted. Type them ``ListenOptions``.
* ``dial.dub`` is a list of dub verbs without ``verb``: ``list[Nested[Dub]]``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, Literal, TypeAlias

from pydantic import (
    MISSING,
    Discriminator,
    GetJsonSchemaHandler,
    StrictBool,
    StrictFloat,
    StrictInt,
    Tag,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from jambonz._wire import WireModel
from jambonz.types import Auth, Hook, MixType
from jambonz.verbs._base import Nested, VerbModel
from jambonz.verbs.shared import Synthesizer

__all__ = [
    "BidirectionalAudio",
    "Dub",
    "DubSay",
    "Listen",
    "ListenOptions",
    "NestedListen",
    "NestedStream",
    "Stream",
]


class BidirectionalAudio(WireModel):
    """Whether and how the websocket server may send audio back into the call.

    jambonz starts from ``{"enabled": true}`` (or ``false`` with the deprecated
    ``disableBidirectionalAudio``) and merges this object over it, so leaving it
    out keeps bidirectional audio on.
    """

    enabled: StrictBool | MISSING = MISSING
    streaming: StrictBool | MISSING = MISSING
    """Raw audio frames streamed back, instead of complete audio messages."""
    sample_rate: StrictInt | StrictFloat | MISSING = MISSING


class _ListenCommon(WireModel):
    """Fields shared by the ``listen`` verb and ``config.listen`` (``ListenOptions``)."""

    sample_rate: StrictInt | StrictFloat | MISSING = MISSING
    """Hz; jambonz uses 8000 when unset. Not a closed set (8000, 16000, 24000...)."""
    ws_auth: Auth | MISSING = MISSING
    """Basic auth credentials for the websocket connection."""
    mix_type: MixType | MISSING = MISSING
    """jambonz uses ``mono`` when unset."""
    metadata: dict[str, Any] | MISSING = MISSING
    """Sent to the websocket server in the initial message (merged with call info)."""
    max_length: StrictInt | StrictFloat | MISSING = MISSING
    """Seconds; the stream is closed after this long."""
    pass_dtmf: StrictBool | MISSING = MISSING
    play_beep: StrictBool | MISSING = MISSING
    disable_bidirectional_audio: StrictBool | MISSING = MISSING
    """Deprecated: use ``bidirectional_audio=BidirectionalAudio(enabled=False)``."""
    bidirectional_audio: BidirectionalAudio | MISSING = MISSING
    timeout: StrictInt | StrictFloat | MISSING = MISSING


class _ListenVerb(VerbModel, _ListenCommon):
    """Fields of ``listen`` and its alias ``stream`` (only the ``verb`` literal differs)."""

    url: str
    """The ws:// or wss:// URL that receives the audio."""
    action_hook: Hook | MISSING = MISSING
    """Called when the stream ends. Docs mark it required; specs.json and the
    official schema do not, so it is optional here."""
    finish_on_key: str | MISSING = MISSING
    early_media: StrictBool | MISSING = MISSING
    """Stream before the call is answered."""
    channel: StrictInt | StrictFloat | MISSING = MISSING
    """Inside ``dial``, ``2`` streams the caller's leg instead of the called party's."""
    auth: Auth | MISSING = MISSING
    """Legacy name accepted by specs.json. feature-server reads it but only uses
    ``ws_auth`` for the connection: prefer ``ws_auth``."""


class Listen(_ListenVerb):
    """Stream the call's audio to a websocket server (optionally bidirectional).

    Also accepted (sent without ``verb``) by ``dial.listen``/``dial.stream`` and
    ``conference.listen``/``conference.stream``. Not modelled yet: ``transcribe``
    (nested transcribe); use ``extra_fields`` for it.
    """

    verb: Literal["listen"] = "listen"


class Stream(_ListenVerb):
    """Synonym of ``listen`` (added in Jan 2025, feature-server PR #1045).

    jambonz runs it as a ``listen`` task: ``validateVerb`` renames it first (its
    ``verbTransforms``) and the docs URL ``/verbs/stream`` redirects to ``listen``.
    Verified live as a verb, in ``dial.stream`` and in ``conference.stream``;
    nested there the name does not matter (it is sent without ``verb``). Not in
    ``config``: see ``Config``.
    """

    verb: Literal["stream"] = "stream"


def _listen_tag(default: Literal["listen", "stream"]) -> Callable[[Any], str]:
    def tag(value: Any) -> str:
        name = value.get("verb") if isinstance(value, dict) else getattr(value, "verb", None)
        return name if name in ("listen", "stream") else default

    return tag


class _AnyOfSchema:
    """``Annotated`` marker: publish the union as ``anyOf`` instead of ``oneOf``.

    Both members accept (and, nested, emit) the same object, so ``oneOf`` would
    make every value invalid against the JSON schema. Documentation only.
    """

    def __get_pydantic_json_schema__(
        self, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = dict(handler(core_schema))
        if "oneOf" in schema:
            schema["anyOf"] = schema.pop("oneOf")
        return schema


NestedListen: TypeAlias = Annotated[
    Annotated[Nested[Listen], Tag("listen")] | Annotated[Nested[Stream], Tag("stream")],
    Discriminator(_listen_tag("listen")),
    _AnyOfSchema(),
]
"""A ``Listen`` or ``Stream`` nested in another verb (no ``verb`` on the wire).

Wire input without ``verb`` parses as ``Listen``; a matching ``"verb"`` key picks
the class. Used for ``dial.listen`` and ``conference.listen``.
"""

NestedStream: TypeAlias = Annotated[
    Annotated[Nested[Listen], Tag("listen")] | Annotated[Nested[Stream], Tag("stream")],
    Discriminator(_listen_tag("stream")),
    _AnyOfSchema(),
]
"""Like ``NestedListen``, but wire input without ``verb`` parses as ``Stream``
(for ``dial.stream``, so that ``Dial(stream=Stream(...))`` round-trips)."""


class ListenOptions(_ListenCommon):
    """``config.listen`` / ``config.stream``: start or stop a background listen.

    With ``enable=True`` jambonz starts a background ``listen`` with the other
    fields (so ``url`` is needed then, although no schema requires it); with
    ``enable=False`` it stops the running one. Not the shape of ``dial.listen``,
    which is a nested ``Listen``.
    """

    enable: StrictBool
    url: str | MISSING = MISSING


class DubSay(WireModel):
    """Object form of ``dub.say``: text plus an optional synthesizer.

    feature-server reads only ``say.text`` and ``say.synthesizer``; without a
    synthesizer the application's default voice is used. Of the synthesizer it
    reads only ``vendor``, ``language``, ``voice`` and ``label``, and falls back to
    the session value for each one missing or ``"default"``. jambonz accepts a
    synthesizer without ``vendor`` here, but ``Synthesizer`` requires it: pass
    ``vendor="default"`` to keep the session vendor and change e.g. only the voice.
    """

    text: str
    synthesizer: Synthesizer | MISSING = MISSING


class Dub(VerbModel):
    """Add, remove, silence or play/speak on an extra audio track mixed into the call.

    Tracks are heard by the party on whose leg they are created: top level is
    the caller, ``dial.dub`` (``list[Nested[Dub]]``) the called party.
    """

    verb: Literal["dub"] = "dub"
    action: Literal["addTrack", "removeTrack", "silenceTrack", "playOnTrack", "sayOnTrack"]
    track: str
    play: str | MISSING = MISSING
    """Audio URL, for ``playOnTrack`` (or ``addTrack`` which then plays it)."""
    say: str | DubSay | MISSING = MISSING
    """Text to speak, for ``sayOnTrack`` (or ``addTrack`` which then speaks it)."""
    loop: StrictBool | MISSING = MISSING
    gain: StrictInt | StrictFloat | str | MISSING = MISSING
    """dB as a number or a string such as ``"-6 dB"``; a string without ``dB``
    is silently treated as 0 by jambonz."""
