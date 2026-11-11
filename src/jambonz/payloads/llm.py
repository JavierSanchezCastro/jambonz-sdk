"""Payloads of ``llm``/``agent`` hooks (actionHook, toolHook) and the tool-hook response."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import MISSING, AliasChoices, BaseModel, ConfigDict, Field

from jambonz.payloads.call import CallInfo
from jambonz.payloads.transfer import TransferOutcome, TransferReason

LLMCompletionReason: TypeAlias = Literal[
    "normal conversation end",
    "connection failure",
    "disconnect from remote end",
    "server failure",
    "server error",
    "client error calling function",
    "client error calling mcp function",
]


class LLMResult(CallInfo):
    """Body of ``llm``'s actionHook (the session ended).

    ``completion_reason`` lists the 7 official values (not captured live yet);
    the docs also mention a parametrised ``session closed: <reason>`` and
    ``hangup``, which the open ``str`` accepts. ``error`` is set on a server
    error. On an llm/agent handoff the docs report the transfer outcome in
    ``transfer_result``/``transfer_reason``.
    """

    completion_reason: LLMCompletionReason | str | None = None
    error: Any = None
    transfer_result: TransferOutcome | str | None = None
    transfer_reason: TransferReason | str | None = None


class ToolCall(CallInfo):
    """Body of ``llm``'s toolHook (a tool/function call from the model).

    ``llm`` and the tool-hook POST send the arguments as ``args``; ``agent`` (and
    the AsyncAPI ``llm:tool-call``) send ``arguments``. Both land in ``args`` and a
    model dump writes ``args``. Argument keys are passed through untouched.

    ``call_id`` is the envelope's SIP Call-ID, never the tool call id (that is
    ``tool_call_id``). Vendor extras such as Google's ``function_calls`` stay in
    ``model_extra``.
    """

    tool_call_id: str | None = None
    name: str | None = None
    args: dict[str, Any] | None = Field(
        default=None,
        validation_alias=AliasChoices("args", "arguments"),
        serialization_alias="args",
    )


class ToolResult(BaseModel):
    """Response body for an ``llm`` toolHook request.

    The shape is vendor-specific; feature-server only adds defaults when the body
    has no ``type``:

    * Ultravox-style (default): ``ToolResult(result=...)``; jambonz fills in
      ``type: "client_tool_result"`` and ``invocation_id``.
    * OpenAI realtime: pass the vendor envelope as extra keys and no ``result``,
      e.g. ``ToolResult.model_validate({"type": "conversation.item.create",
      "item": {...}})`` (``model_validate`` keeps type checkers happy with
      keys the model does not declare).

    Extra keys are allowed and sent as given; ``result`` is omitted when unset.
    """

    model_config = ConfigDict(extra="allow")

    result: Any | MISSING = MISSING
