"""Models for what jambonz sends to your app: HTTP hook bodies and websocket frames.

* the call envelope (:class:`CallInfo`) and the application's ``call_hook``
  (:class:`CallWebhook`) and ``call_status_hook`` (:class:`CallStatusEvent`);
* one model per verb hook (``GatherResult``, ``DialResult``, ``AmdEvent``,
  ``ConferenceStatusEvent``, ``EnqueueResult``...);
* the camelCase listen/conference.listen websocket frames
  (:class:`ListenMetadata`, :class:`ConferenceListenEvent`,
  :func:`parse_listen_message`).

Every model keeps unknown keys (``model_extra``) and types enums as
``Literal[known values] | str``, so a new value from jambonz never fails validation.
"""

from jambonz.payloads._base import Payload
from jambonz.payloads.amd import AmdEvent, AmdType
from jambonz.payloads.call import (
    CallDefaults,
    CallDirection,
    CallInfo,
    CallStatusEvent,
    CallStatusValue,
    CallTerminationBy,
    CallWebhook,
    SipInvite,
)
from jambonz.payloads.conference import (
    ConferenceResult,
    ConferenceStatusEvent,
    ConferenceWait,
)
from jambonz.payloads.dial import (
    DialDtmfEvent,
    DialHoldEvent,
    DialReferEvent,
    DialResult,
    HoldDetail,
    ReferDetails,
)
from jambonz.payloads.gather import (
    GatherPartialResult,
    GatherReason,
    GatherResult,
    SpeechAlternative,
    SpeechResult,
    SpeechTranscript,
    SpeechVendor,
)
from jambonz.payloads.listen import (
    ConferenceListenEvent,
    ConferenceListenEventType,
    ListenDtmfEvent,
    ListenMessage,
    ListenMetadata,
    ListenResult,
    parse_listen_message,
)
from jambonz.payloads.llm import LLMCompletionReason, LLMResult, ToolCall, ToolResult
from jambonz.payloads.play import PlayReason, PlayResult, PlayStatus
from jambonz.payloads.queues import (
    DequeueOutcome,
    DequeueResult,
    EnqueueOutcome,
    EnqueueResult,
    EnqueueWait,
)
from jambonz.payloads.sip import (
    SipReferEvent,
    SipReferEventType,
    SipReferResult,
    SipRequestOutcome,
    SipRequestResult,
)
from jambonz.payloads.transfer import TransferOutcome, TransferReason, TransferResult
from jambonz.types import ConferenceStatusEventName, MixType

__all__ = [
    "AmdEvent",
    "AmdType",
    "CallDefaults",
    "CallInfo",
    "CallStatusValue",
    "CallStatusEvent",
    "CallTerminationBy",
    "CallWebhook",
    "ConferenceStatusEventName",
    "ConferenceListenEvent",
    "ConferenceListenEventType",
    "ConferenceResult",
    "ConferenceStatusEvent",
    "ConferenceWait",
    "DequeueOutcome",
    "DequeueResult",
    "DialDtmfEvent",
    "DialHoldEvent",
    "DialReferEvent",
    "DialResult",
    "CallDirection",
    "EnqueueResult",
    "EnqueueWait",
    "GatherPartialResult",
    "GatherReason",
    "GatherResult",
    "HoldDetail",
    "LLMCompletionReason",
    "LLMResult",
    "ListenDtmfEvent",
    "ListenMessage",
    "ListenMetadata",
    "ListenResult",
    "MixType",
    "Payload",
    "PlayReason",
    "PlayResult",
    "PlayStatus",
    "EnqueueOutcome",
    "ReferDetails",
    "SipInvite",
    "SipReferEvent",
    "SipReferEventType",
    "SipReferResult",
    "SipRequestOutcome",
    "SipRequestResult",
    "SpeechAlternative",
    "SpeechResult",
    "SpeechTranscript",
    "SpeechVendor",
    "ToolCall",
    "ToolResult",
    "TransferOutcome",
    "TransferReason",
    "TransferResult",
    "parse_listen_message",
]
