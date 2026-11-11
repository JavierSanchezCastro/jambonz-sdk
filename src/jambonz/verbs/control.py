"""Small call-control verbs: pause, hangup, redirect, answer, leave, alert, dtmf, tag."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import MISSING, Field, StrictFloat, StrictInt

from jambonz.types import Hook
from jambonz.verbs._base import VerbModel


class Pause(VerbModel):
    """Wait ``length`` seconds (required, no default)."""

    verb: Literal["pause"] = "pause"
    length: StrictInt | StrictFloat


class Hangup(VerbModel):
    """Hang up the call, optionally adding SIP headers to the BYE."""

    verb: Literal["hangup"] = "hangup"
    headers: dict[str, str] | MISSING = MISSING


class Redirect(VerbModel):
    """Fetch a new verb list from ``action_hook`` and continue with it."""

    verb: Literal["redirect"] = "redirect"
    action_hook: Hook
    status_hook: Hook | MISSING = MISSING


class Answer(VerbModel):
    """Answer the call (jambonz answers on the first media verb anyway)."""

    verb: Literal["answer"] = "answer"


class Leave(VerbModel):
    """Leave the current conference or queue and continue with the next verb.

    Only inside a conference/queue: elsewhere jambonz.cloud fails the task and drops
    the remaining verbs (checked 2026-11-09).
    """

    verb: Literal["leave"] = "leave"


class Alert(VerbModel):
    """Raise an alert in the jambonz account (portal and ``Alerts`` API) with ``message``.

    Checked live: it does not send anything to the caller.
    """

    verb: Literal["alert"] = "alert"
    message: str


class Dtmf(VerbModel):
    """Send DTMF digits to the caller (RFC 2833), ``duration`` ms per digit.

    Digits ``0-9``, ``*``, ``#`` and ``A-D`` (lowercase too: jambonz sends them as
    uppercase). Checked live; the jambonz docs only mention the first twelve.

    No ``w``/``W`` pauses: the official SDK documents ``w`` as a 500 ms pause, but
    jambonz.cloud fails the whole verb ("error sending dtmf", no digit is sent).
    """

    verb: Literal["dtmf"] = "dtmf"
    dtmf: Annotated[str, Field(pattern=r"^[0-9A-Da-d*#]+$")]
    duration: StrictInt | StrictFloat | MISSING = MISSING


class Tag(VerbModel):
    """Attach ``data`` to the call; later webhooks carry it as ``customerData``.

    Each ``tag`` replaces the whole collection. Keys inside ``data`` go out as given.
    """

    verb: Literal["tag"] = "tag"
    data: dict[str, Any]
