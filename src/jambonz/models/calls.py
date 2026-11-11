from enum import Enum

from pydantic import ConfigDict, Field

from jambonz.models._base import Sid, _JambonzModel


class CallStatus(str, Enum):
    """Call status in REST responses (closed ``Enum``).

    Hook payloads type the same field as the open ``Literal``
    ``jambonz.CallStatusValue`` instead. Both include ``early-media``;
    ``ALERTING`` is kept for compatibility with earlier releases.
    """

    TRYING = "trying"
    RINGING = "ringing"
    EARLY_MEDIA = "early-media"
    ALERTING = "alerting"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    BUSY = "busy"
    NO_ANSWER = "no-answer"
    FAILED = "failed"
    QUEUED = "queued"


class Direction(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Call(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-call-control/calls/list-calls"""

    account_sid: Sid | None = None
    call_id: str | None = None
    call_sid: Sid | None = None
    call_status: CallStatus | None = None
    direction: Direction | None = None
    from_: str | None = Field(None, alias="from")
    service_url: str | None = None
    sip_status: int | None = None
    to: str | None = None
    application_sid: Sid | None = None
    caller_name: str | None = None
    duration: int | None = None
    originating_sip_trunk_name: str | None = None
    parent_call_sid: Sid | None = None

    model_config = ConfigDict(populate_by_name=True)


class RecentCall(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/recent-calls/list-recent-calls"""

    call_sid: Sid | None = None
    account_sid: Sid | None = None
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    answered: bool | None = None
    sip_call_id: str | None = None
    sip_status: int | None = None
    duration: int | None = None
    attempted_at: int | str | None = None
    answered_at: int | str | None = None
    terminated_at: int | str | None = None
    termination_reason: str | None = None
    host: str | None = None
    remote_host: str | None = None
    direction: Direction | None = None
    trunk: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class CallTarget(_JambonzModel):
    """Target for dialing: phone number, SIP URI, user, or teams."""

    type: str
    number: str | None = None
    sip_uri: str | None = Field(None, alias="sipUri")
    name: str | None = None

    model_config = ConfigDict(populate_by_name=True)
