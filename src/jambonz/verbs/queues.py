"""Queues and conferences: enqueue, dequeue, conference (plus its record option)."""

from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import Annotated, Any, Literal

from pydantic import MISSING, Field, StrictBool, StrictFloat, StrictInt, field_validator

from jambonz._wire import WireModel
from jambonz.types import ConferenceStatusEventName, Hook, JambonzWarning
from jambonz.verbs._base import VerbModel
from jambonz.verbs.media import NestedListen, NestedStream

_END_TALKING = (
    "use 'stop-talking': jambonz never sends 'end-talking' (a typo in its docs; "
    "conference.js has always used 'stop-talking')"
)


class Enqueue(VerbModel):
    """Put the caller in the named queue until a ``dequeue`` bridges it or it leaves.

    ``wait_hook`` is called on entry and again after each response is played;
    its response may contain only ``say``, ``play``, ``pause``, ``leave`` and
    ``tag`` (anything else makes feature-server end the wait with an error).
    ``action_hook`` is called when the caller leaves the queue (bridged, hung
    up, ``leave`` or error). On jambonz.cloud the ``wait_hook`` body carries only
    ``queue_sid``, ``queue_time``, ``queue_size``, ``queue_position``, ``call_sid``
    and ``call_id`` (no ``from``/``to``), and a ``leave`` from it ends the
    enqueue with ``queue_result: "leave"``.

    ``priority``: lower is dequeued first (docs: 0-999, default 999). Verified
    live: jambonz orders by the exact number, decimals included (2.5 before 2.6),
    and accepts values above 999 (sorted after the default). Those are allowed
    but raise a ``JambonzWarning``. Negative values are rejected (feature-server
    logs a warning for them).
    """

    verb: Literal["enqueue"] = "enqueue"
    name: str
    action_hook: Hook | MISSING = MISSING
    wait_hook: Hook | MISSING = MISSING
    priority: Annotated[StrictInt, Field(ge=0)] | Annotated[StrictFloat, Field(ge=0)] | MISSING = (
        MISSING
    )

    @field_validator("priority")
    @classmethod
    def _warn_priority_above_999(cls, value: Any) -> Any:
        if isinstance(value, int | float) and value > 999:
            warnings.warn(
                f"enqueue priority {value} is outside the documented range 0-999; "
                "jambonz accepts it and dequeues it after the default 999",
                JambonzWarning,
                stacklevel=2,
            )
        return value


class Dequeue(VerbModel):
    """Take a caller out of the named queue and bridge it to this call.

    Without ``call_sid`` the first caller (by priority) is taken; with it, that
    specific call. ``timeout`` is in seconds; when unset or 0 jambonz waits
    forever for someone to enter the queue. ``beep`` plays a tone when the
    calls are connected. ``action_hook`` receives ``dequeue_result``
    (``complete``, ``timeout``, ``hangup``), but feature-server does not wait for
    it: when the bridge ends the session goes on to the next verb (or hangs up),
    and the hook's response is ignored (verified on jambonz.cloud). Put follow-up
    verbs after ``dequeue`` instead.
    """

    verb: Literal["dequeue"] = "dequeue"
    name: str
    action_hook: Hook | MISSING = MISSING
    timeout: StrictInt | StrictFloat | MISSING = MISSING
    beep: StrictBool | MISSING = MISSING
    call_sid: str | MISSING = MISSING


class ConferenceRecord(WireModel):
    """``conference.record``: record the conference to a file on the media server.

    feature-server runs ``conference <name> record <path>`` when this caller
    starts the conference. Only in specs.json (the docs do not mention it).
    """

    path: str


class Conference(VerbModel):
    """Join the caller to a named conference room (created on first use).

    With ``start_conference_on_enter=False`` the caller waits (hearing
    ``wait_hook``) until a moderator starts the conference. ``wait_hook`` and
    ``enter_hook`` responses may contain only ``say``, ``play`` and ``pause``
    (verified: a ``leave`` there makes jambonz stop calling ``wait_hook`` and the
    caller keeps waiting; ``leave`` is for ``enqueue`` only).
    ``status_hook`` receives only the events listed in ``status_events``, and
    nothing at all unless both are set.

    ``listen`` (or its synonym ``stream``) streams the room's mixed audio to a
    websocket: a virtual participant joins and sends the audio as binary frames,
    plus conference events (``start-talking``, ``participant-join``...) as JSON text
    messages on the same socket (verified live).

    Surprises in feature-server: ``end_conference_duration`` is sent to
    FreeSWITCH as ``endconference_grace_time`` (seconds the conference stays up
    after the ``end_conference_on_exit`` member leaves), not a maximum duration
    as the official schema says; and ``max_participants`` only applies when
    greater than 1.
    """

    verb: Literal["conference"] = "conference"
    name: str
    beep: StrictBool | MISSING = MISSING
    member_tag: str | MISSING = MISSING
    speak_only_to: str | MISSING = MISSING
    """Coach mode: this member is heard only by the member with this tag."""
    start_conference_on_enter: StrictBool | MISSING = MISSING
    end_conference_on_exit: StrictBool | MISSING = MISSING
    end_conference_duration: StrictInt | StrictFloat | MISSING = MISSING
    max_participants: StrictInt | MISSING = MISSING
    join_muted: StrictBool | MISSING = MISSING
    action_hook: Hook | MISSING = MISSING
    wait_hook: Hook | MISSING = MISSING
    status_events: Sequence[ConferenceStatusEventName] | MISSING = MISSING
    status_hook: Hook | MISSING = MISSING
    enter_hook: Hook | MISSING = MISSING
    record: ConferenceRecord | MISSING = MISSING
    listen: NestedListen | MISSING = MISSING
    stream: NestedStream | MISSING = MISSING
    """Synonym of ``listen`` (verified live; not in specs.json 0.1.13)."""
    distribute_dtmf: StrictBool | MISSING = MISSING

    @field_validator("status_events", mode="before")
    @classmethod
    def _explain_end_talking(cls, value: Any) -> Any:
        if isinstance(value, list | tuple) and "end-talking" in value:
            raise ValueError(_END_TALKING)
        return value
