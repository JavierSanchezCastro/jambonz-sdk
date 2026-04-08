# Webhooks

## Outgoing: Response verbs

When jambonz sends a webhook to your server, you respond with a list of verbs:

```python
from jambonz import JambonzResponse, Say, Gather, Hangup, Input

@app.post("/incoming-call")
def handle_call() -> JambonzResponse:
    return [
        Say(text="Hello!"),
        Gather(input=[Input.SPEECH], action_hook="/speech"),
    ]
```

### Available verbs

| Verb | Description |
|---|---|
| `Say` | Text-to-speech |
| `Play` | Play audio URL |
| `Gather` | Collect speech or DTMF input |
| `Pause` | Wait |
| `Hangup` | End the call |
| `Redirect` | Transfer to another webhook |
| `LLM` | Connect to conversational AI (ElevenLabs, OpenAI) |
| `Dial` | Dial out to a number |

### Serialization

`JambonzResponse` automatically handles:

- Excludes null fields (jambonz rejects nulls)
- Converts to camelCase (`action_hook` -> `actionHook`)
- Serializes enums (`Input.SPEECH` -> `"speech"`)

```python
# Works with any framework
response = JambonzResponse([Say(text="Hi"), Hangup()])
response.model_dump()       # -> list[dict]
response.model_dump_json()  # -> str
```

## Incoming: Parsing webhooks

Typed models for every webhook jambonz sends:

### New call

```python
from jambonz import CallWebhook

@app.post("/incoming-call")
def handle(call: CallWebhook) -> JambonzResponse:
    print(call.from_)       # caller number
    print(call.to)          # called number
    print(call.direction)   # Direction.INBOUND
    print(call.call_sid)    # UUID
```

### Call status

```python
from jambonz import CallStatusEvent

@app.post("/call-status")
def handle(event: CallStatusEvent):
    print(event.call_status)  # CallStatus.COMPLETED
    print(event.duration)
```

### Gather result

```python
from jambonz import GatherResult

@app.post("/gather-result")
def handle(result: GatherResult) -> JambonzResponse:
    print(result.transcript)  # shortcut to best transcript
    print(result.reason)      # "speechDetected", "dtmfDetected", "timeout"
    print(result.digits)      # DTMF digits if any
```

### Dial result

```python
from jambonz import DialResult

@app.post("/dial-result")
def handle(result: DialResult):
    print(result.dial_call_status)  # "completed", "failed", "busy"
    print(result.dial_sip_status)   # SIP status code
```

### LLM session end

```python
from jambonz import LLMResult

@app.post("/llm-complete")
def handle(result: LLMResult):
    print(result.completion_reason)
```

### LLM tool call

```python
from jambonz import ToolCall, ToolResult

@app.post("/tool-call")
def handle(tool: ToolCall) -> ToolResult:
    print(tool.name)
    print(tool.args)
    return ToolResult(
        tool_call_id=tool.tool_call_id,
        result="done",
    )
```
