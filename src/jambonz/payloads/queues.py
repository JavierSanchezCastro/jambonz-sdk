"""Payloads of ``enqueue``/``dequeue`` hooks (actionHooks and the enqueue waitHook)."""

from __future__ import annotations

from typing import Literal, TypeAlias

from jambonz.payloads._base import Payload
from jambonz.payloads.call import CallInfo

__all__ = [
    "DequeueOutcome",
    "EnqueueOutcome",
    "DequeueResult",
    "EnqueueResult",
    "EnqueueWait",
]

EnqueueOutcome: TypeAlias = Literal["bridged", "hangup", "leave", "error"]
"""Why the call left the queue (``queue_result`` of enqueue's actionHook)."""

DequeueOutcome: TypeAlias = Literal["complete", "timeout", "hangup", "error"]
"""Outcome of a dequeue (official: complete/timeout/hangup; docs add ``error``)."""


class EnqueueResult(CallInfo):
    """Body of ``enqueue``'s actionHook: the call left the queue (live + official schema).

    ``queue_sid`` has the form ``queue:<account_sid>:<name>`` and ``queue_time``
    is the number of seconds spent in the queue.

    On ``hangup``/``bridged`` the call may already be over: live payloads then
    carry ``call_status`` ``completed`` plus ``duration`` and
    ``call_termination_by`` in the envelope. Docs spell the keys in camelCase
    (``queueSid``...); the wire is snake_case. ``queue_size``/``queue_position``
    are only sent on the waitHook (see ``EnqueueWait``), despite the docs.
    """

    queue_sid: str
    queue_time: int
    queue_result: EnqueueOutcome | str


class EnqueueWait(Payload):
    """Body of ``enqueue``'s waitHook (live + official schema).

    Sparse: jambonz sends only these six keys (official: NOT the base call
    payload), so this does not inherit ``CallInfo``. Reply with verbs to play
    while the caller waits (``leave`` exits the queue). ``queue_position`` is
    0-based.
    """

    queue_sid: str
    queue_time: int
    queue_size: int | None = None
    queue_position: int | None = None
    call_sid: str | None = None
    call_id: str | None = None


class DequeueResult(CallInfo):
    """Body of ``dequeue``'s actionHook (live + official schema).

    feature-server does not await this hook: the response is ignored and the
    next verb runs anyway. When the bridged call has already ended, the
    envelope carries ``call_status`` ``completed``, ``duration`` and
    ``call_termination_by`` (live).
    """

    dequeue_result: DequeueOutcome | str
