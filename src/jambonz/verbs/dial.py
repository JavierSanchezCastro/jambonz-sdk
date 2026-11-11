from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated, Any, Literal

from pydantic import MISSING, Field, StrictBool, StrictFloat, StrictInt

from jambonz._wire import WireModel
from jambonz.types import Auth, Hook
from jambonz.verbs._base import Nested, VerbModel
from jambonz.verbs.components import Amd
from jambonz.verbs.media import Dub, NestedListen, NestedStream


class DialFrom(WireModel):
    """Override the From header of the outbound leg."""

    user: str | MISSING = MISSING
    host: str | MISSING = MISSING


class _TargetBase(WireModel):
    confirm_hook: Hook | MISSING = MISSING
    method: Literal["GET", "POST"] | MISSING = MISSING
    headers: dict[str, str] | MISSING = MISSING
    from_: DialFrom | MISSING = Field(
        default=MISSING, validation_alias="from", serialization_alias="from"
    )
    override_to: str | MISSING = MISSING


class PhoneTarget(_TargetBase):
    type: Literal["phone"] = "phone"
    number: str
    trunk: str | MISSING = MISSING


class SipTarget(_TargetBase):
    type: Literal["sip"] = "sip"
    sip_uri: str
    auth: Auth | MISSING = MISSING
    proxy: str | MISSING = MISSING


class UserTarget(_TargetBase):
    type: Literal["user"] = "user"
    name: str


class TeamsTarget(_TargetBase):
    type: Literal["teams"] = "teams"
    number: str
    tenant: str | MISSING = MISSING
    vmail: StrictBool | MISSING = MISSING


Target = Annotated[PhoneTarget | SipTarget | UserTarget | TeamsTarget, Field(discriminator="type")]
"""A ``dial`` destination, discriminated on ``type``."""


class DtmfCapture(WireModel):
    """Per-leg DTMF patterns for ``Dial.dtmf_capture`` (the object form).

    ``child_call`` patterns are matched on the called party's leg, ``parent_call``
    on the caller's. Caveat: feature-server 0.9.x (``parseDtmfOptions`` in
    ``tasks/dial.js``) adds ``parentCall`` patterns to the *child* leg collector
    too, so with this form both lists end up watching the called party. To watch
    both legs use the plain list form of ``dtmf_capture``.
    """

    child_call: Sequence[str] | MISSING = MISSING
    parent_call: Sequence[str] | MISSING = MISSING


class Dial(VerbModel):
    """Bridge the call to one or more targets (rung simultaneously).

    ``listen``/``stream`` fork the bridged audio to a websocket (a listen verb
    without ``"verb"``; jambonz uses ``listen`` if both are set). ``dub`` adds
    dubbing tracks, ``amd`` runs answering machine detection on the called party.
    ``dtmf_capture`` is only honoured together with ``dtmf_hook``: a list of
    patterns watches both legs, a ``DtmfCapture`` sets them per leg.

    ``transcribe`` is not modelled yet; use ``extra_fields`` for it.
    """

    verb: Literal["dial"] = "dial"
    target: Sequence[Target] = Field(min_length=1, max_length=10)
    action_hook: Hook | MISSING = MISSING
    on_hold_hook: Hook | MISSING = MISSING
    answer_on_bridge: StrictBool | MISSING = MISSING
    caller_id: str | MISSING = MISSING
    caller_name: str | MISSING = MISSING
    confirm_hook: Hook | MISSING = MISSING
    refer_hook: Hook | MISSING = MISSING
    dial_music: str | MISSING = MISSING
    dtmf_hook: Hook | MISSING = MISSING
    headers: dict[str, str | StrictInt | StrictFloat] | MISSING = MISSING
    anchor_media: StrictBool | MISSING = MISSING
    exit_media_path: StrictBool | MISSING = MISSING
    boost_audio_signal: StrictInt | StrictFloat | str | MISSING = MISSING
    time_limit: StrictInt | StrictFloat | MISSING = MISSING
    timeout: StrictInt | StrictFloat | MISSING = MISSING
    proxy: str | MISSING = MISSING
    tag: dict[str, Any] | MISSING = MISSING
    forward_pai: StrictBool | MISSING = Field(
        default=MISSING, validation_alias="forwardPAI", serialization_alias="forwardPAI"
    )
    srtp_encryption: Literal["sdes", "dtls"] | MISSING = MISSING
    amd: Amd | MISSING = MISSING
    listen: NestedListen | MISSING = MISSING
    """A ``Listen`` (or ``Stream``) sent without ``"verb"``."""
    stream: NestedStream | MISSING = MISSING
    """Synonym of ``listen`` (same shape: specs.json types both ``#listen``; dial.js
    reads ``listen || stream``). Takes a ``Stream`` or a ``Listen``."""
    dub: Sequence[Nested[Dub]] | MISSING = MISSING
    dtmf_capture: Sequence[str] | DtmfCapture | MISSING = MISSING
    codecs: Sequence[str] | MISSING = MISSING
    """Documented on docs.jambonz.org but absent from @jambonz/verb-specifications
    0.1.13: a jambonz that enforces that validator rejects the verb with
    "dial: unknown property codecs". Not yet checked against jambonz.cloud (e2e)."""
