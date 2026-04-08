from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _JambonzBase(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Input(str, Enum):
    SPEECH = "speech"
    DIGITS = "digits"
    DTMF = "dtmf"


class Synthesizer(_JambonzBase):
    vendor: str
    language: str
    voice: str | None = None
    label: str | None = None


class Recognizer(_JambonzBase):
    vendor: str
    language: str
    label: str | None = None


class Say(_JambonzBase):
    verb: Literal["say"] = "say"
    text: str
    synthesizer: Synthesizer | None = None


class Play(_JambonzBase):
    verb: Literal["play"] = "play"
    url: str


class Gather(_JambonzBase):
    verb: Literal["gather"] = "gather"
    input: list[Input] = [Input.SPEECH]
    action_hook: str | None = None
    timeout: int = 10
    recognizer: Recognizer | None = None
    say: Say | None = None
    play: Play | None = None
    num_digits: int | None = None


class Pause(_JambonzBase):
    verb: Literal["pause"] = "pause"
    length: float = 1.0


class Hangup(_JambonzBase):
    verb: Literal["hangup"] = "hangup"


class Redirect(_JambonzBase):
    verb: Literal["redirect"] = "redirect"
    action_hook: str


class LLMAuth(_JambonzBase):
    agent_id: str | None = None
    api_key: str | None = None


class LLM(_JambonzBase):
    verb: Literal["llm"] = "llm"
    vendor: str
    auth: LLMAuth | None = None
    model: str | None = None
    llm_options: dict[str, Any] | None = None
    action_hook: str | None = None
    tool_hook: str | None = None
    event_hook: str | None = None
    events: list[str] | None = None


class Dial(_JambonzBase):
    verb: Literal["dial"] = "dial"
    action_hook: str | None = None
    caller_id: str | None = None
    timeout: int = 60
    target: list[dict[str, Any]] = []


Verb = Annotated[
    Say | Play | Gather | Pause | Hangup | Redirect | LLM | Dial,
    Field(discriminator="verb"),
]
