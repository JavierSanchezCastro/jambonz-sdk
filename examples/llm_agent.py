"""Connect incoming calls to an ElevenLabs conversational AI agent."""
import os

from fastapi import FastAPI

from jambonz import (
    CallWebhook,
    LLMResult,
    ToolCall,
    ToolResult,
    JambonzResponse,
    LLM,
    LLMAuth,
)

app = FastAPI()

AGENT_ID = os.environ.get("ELEVENLABS_AGENT_ID", "your-agent-id")


@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    print(f"Call from {call.from_} to {call.to}")
    return [
        LLM(
            vendor="elevenlabs",
            auth=LLMAuth(agent_id=AGENT_ID),
            llm_options={},
            action_hook="/llm-complete",
            tool_hook="/tool-call",
        ),
    ]


@app.post("/llm-complete")
def handle_llm_complete(result: LLMResult):
    print(f"LLM session ended: {result.completion_reason}")


@app.post("/tool-call")
def handle_tool(tool: ToolCall) -> ToolResult:
    print(f"Tool call: {tool.name}({tool.args})")
    return ToolResult(
        tool_call_id=tool.tool_call_id,
        result="Tool executed successfully.",
    )
