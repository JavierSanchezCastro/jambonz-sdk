from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

from pydantic import MISSING

from jambonz.types import Hook
from jambonz.verbs._base import VerbModel


class LLM(VerbModel):
    """Connect the call to a speech-to-speech LLM (``vendor`` is an open string).

    ``auth``, ``connect_options`` and ``llm_options`` are vendor-specific and go
    out exactly as given (their keys are never camelCased). ``llm_options`` is
    required: jambonz rejects an ``llm`` verb without ``llmOptions``. Partial model:
    ``mcpServers``, ``handoff`` and the like are not modelled yet.
    """

    verb: Literal["llm"] = "llm"
    vendor: str
    model: str | MISSING = MISSING
    auth: dict[str, Any] | MISSING = MISSING
    connect_options: dict[str, Any] | MISSING = MISSING
    llm_options: dict[str, Any]
    action_hook: Hook | MISSING = MISSING
    event_hook: Hook | MISSING = MISSING
    tool_hook: Hook | MISSING = MISSING
    events: Sequence[str] | MISSING = MISSING
