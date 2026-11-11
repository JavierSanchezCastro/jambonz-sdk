"""Payloads of the listen/stream and conference.listen websocket frames.

Also ``listen``'s actionHook result (:class:`ListenResult`), which is a normal
HTTP hook: snake_case keys plus the call envelope.

The websocket text frames are different: their keys are camelCase
(``sampleRate``, ``callSid``, ``memberId``...) and they do not carry the call
envelope, so they use their own private base (``_WsPayload``) instead of
:class:`~jambonz.payloads.call.CallInfo`. Use :func:`parse_listen_message` to
pick the right model for a decoded frame.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeAlias, get_args

from pydantic import ConfigDict, Field, ModelWrapValidatorHandler, model_validator
from pydantic.alias_generators import to_camel

from jambonz.payloads._base import Payload
from jambonz.payloads.call import CallDirection, CallInfo, CallStatusValue
from jambonz.types import MixType

ConferenceListenEventType: TypeAlias = Literal[
    "participant-join", "participant-leave", "start-talking", "stop-talking"
]
_CONFERENCE_LISTEN_EVENT_TYPES: frozenset[str] = frozenset(get_args(ConferenceListenEventType))
_DTMF_KEYS: frozenset[str] = frozenset({"event", "dtmf", "duration"})


class _WsPayload(Payload):
    """Base for camelCase websocket frames: ``sample_rate`` <-> ``sampleRate``.

    Wire validation (``model_validate``, ``TypeAdapter``) matches the camelCase
    aliases only: the frames are camelCase, so a snake_case key in one can only be
    the verb's user metadata (merged in flat) and must stay in ``model_extra``
    instead of filling a typed field. Keyword construction
    (``ListenMetadata(sample_rate=8000)``) still accepts the Python names.
    Inherits ``extra="allow"``; dumps are camelCase.
    """

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=False)

    def __init__(self, /, **data: Any) -> None:
        __tracebackhide__ = True
        self.__pydantic_validator__.validate_python(
            data, self_instance=self, by_alias=True, by_name=True
        )

    # Not a "custom" __init__ for pydantic: otherwise model_validate would route
    # through it and bind snake_case keys by name again.
    __init__.__pydantic_base_init__ = True  # type: ignore[attr-defined]

    @model_validator(mode="wrap")
    @classmethod
    def _unset_shadowed_fields(cls, data: Any, handler: ModelWrapValidatorHandler[Any]) -> Any:
        """A user key equal to a field's Python name (``account_sid``) lands in
        ``model_extra``, but pydantic also marks that field as set; undo that
        unless the frame carried the field's wire key, so ``exclude_unset``
        dumps do not invent ``"accountSid": null``."""
        model = handler(data)
        if not isinstance(data, Mapping) or not isinstance(model, _WsPayload):
            return model
        shadowed = (model.model_extra or {}).keys() & type(model).model_fields.keys()
        for name in shadowed:
            info = type(model).model_fields[name]
            wire = info.validation_alias if isinstance(info.validation_alias, str) else info.alias
            if wire not in data:
                model.__pydantic_fields_set__.discard(name)
        return model


class ListenResult(CallInfo):
    """Body of ``listen``'s actionHook (the socket closed; source: live + official).

    snake_case HTTP hook with the call envelope. Docs call the duration
    ``duration``, but the wire key is ``dial_call_duration`` (live): do not read
    ``CallInfo.duration`` for it.
    """

    dial_call_duration: int | None = None
    """Seconds the listen/stream lasted (live)."""
    digits: str | None = None
    """The ``finishOnKey`` digit that ended the listen. Verified live: only the
    finish key is reported (``"#"`` after pressing ``12#``), not the digits before it."""


class ListenMetadata(_WsPayload):
    """First text frame on a listen/stream websocket (live; no official schema).

    camelCase, and NOT the call envelope (it is a standalone model). The verb's
    user ``metadata`` keys are merged flat at the top level; they land in
    ``model_extra`` and are returned by :attr:`metadata`.

    Variants seen live:

    * dialed leg (``dial.listen``): ``hasRecording``/``localSipAddress``/
      ``publicIp``/``callerName``/``callerId``/``parentCallSid`` instead of
      ``fs*``/``apiBaseUrl``;
    * ``conference.listen``: the first frame is ONLY the user metadata (no
      ``sampleRate`` nor call fields), so it all lands in :attr:`metadata`,
      except user keys spelled like a wire key of this model (``to``, ``from``,
      ``direction``, or camelCase names such as ``callSid``): those still fill
      the typed field. Snake_case user keys (``call_sid``, ``account_sid``...)
      never do; they always stay in :attr:`metadata`.

    ``originatingSipTrunkName`` is not seen live; it is typed because the docs say
    the frame carries "all call attributes".
    """

    sample_rate: int | None = None
    mix_type: MixType | str | None = None
    call_sid: str | None = None
    call_id: str | None = None
    account_sid: str | None = None
    application_sid: str | None = None
    parent_call_sid: str | None = None
    sbc_callid: str | None = None
    direction: CallDirection | str | None = None
    from_: str | None = Field(default=None, validation_alias="from", serialization_alias="from")
    to: str | None = None
    caller_name: str | None = None
    caller_id: str | None = None
    call_status: CallStatusValue | str | None = None
    sip_status: int | None = None
    sip_reason: str | None = None
    trace_id: str | None = None
    originating_sip_ip: str | None = None
    originating_sip_trunk_name: str | None = None
    fs_sip_address: str | None = None
    fs_public_ip: str | None = None
    api_base_url: str | None = None
    local_sip_address: str | None = None
    public_ip: str | None = None
    has_recording: bool | None = None

    @property
    def metadata(self) -> dict[str, Any]:
        """The user ``metadata`` keys of the verb: every key not bound to a typed
        field (see the class docstring for keys that collide with wire names)."""
        return dict(self.model_extra or {})


class ConferenceListenEvent(_WsPayload):
    """JSON text frame on a ``conference.listen`` websocket (live; no official schema).

    camelCase, standalone (no call envelope). ``type`` values by source: live
    ``participant-join`` and ``start-talking``; docs ``participant-join`` and
    ``participant-leave``; ``stop-talking`` is assumed by symmetry with the
    conference statusHook and has not been captured on the websocket yet.
    """

    type: ConferenceListenEventType | str | None = None
    conference: str | None = None
    """``conf:<account_sid>:<name>``."""
    time: str | None = None
    """ISO-8601 timestamp, kept as ``str``."""
    member_id: int | None = None
    member_type: str | None = None
    """Only on ``participant-join`` (e.g. ``normal``)."""
    channel_uuid: str | None = None
    """Only on ``participant-join``."""
    participants: int | None = None


class ListenDtmfEvent(Payload):
    """DTMF text frame on a listen websocket with ``passDtmf`` (docs only).

    Plain keys (``event``, ``dtmf``, ``duration``); ``duration`` is in RTP
    timestamp units (docs example is the string ``"1600"``).
    """

    event: Literal["dtmf"] | str | None = None
    dtmf: str | None = None
    duration: int | str | None = None


ListenMessage: TypeAlias = ListenMetadata | ConferenceListenEvent | ListenDtmfEvent


def parse_listen_message(data: Mapping[str, Any]) -> ListenMessage:
    """Parse a decoded JSON text frame from a listen/conference.listen websocket.

    Heuristic on the frame's own keys, narrowed to the known shapes:

    * :class:`ConferenceListenEvent` when the frame has ``type`` and
      ``conference``, ``type`` is a known :data:`ConferenceListenEventType` or
      ``conference`` starts with ``conf:``, and ``memberId`` or ``participants``
      is present;
    * :class:`ListenDtmfEvent` when ``event == "dtmf"``, ``dtmf`` is present and
      the frame has no keys besides ``event``/``dtmf``/``duration``;
    * anything else -> :class:`ListenMetadata` (including the metadata-only
      first frame of ``conference.listen``).

    User metadata is free-form, so a metadata frame shaped like an event can
    still be misread. A caller that knows the frame's position on the socket
    (the first text frame is always the metadata) should validate it with
    ``ListenMetadata.model_validate`` directly.
    """
    if _is_conference_event(data):
        return ConferenceListenEvent.model_validate(data)
    if data.get("event") == "dtmf" and "dtmf" in data and data.keys() <= _DTMF_KEYS:
        return ListenDtmfEvent.model_validate(data)
    return ListenMetadata.model_validate(data)


def _is_conference_event(data: Mapping[str, Any]) -> bool:
    if "type" not in data or "conference" not in data:
        return False
    conference = data["conference"]
    known = data["type"] in _CONFERENCE_LISTEN_EVENT_TYPES or (
        isinstance(conference, str) and conference.startswith("conf:")
    )
    return known and ("memberId" in data or "participants" in data)
