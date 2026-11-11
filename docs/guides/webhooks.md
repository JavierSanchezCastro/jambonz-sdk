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

Verbs serialize themselves (`JambonzResponse` is just `Sequence[Verb]`):

- Fields you do not set are omitted; fields that jambonz does not accept as
  `null` do not accept `None` either (`Say(text=None)` is a validation error)
- Converts to camelCase (`action_hook` -> `actionHook`)
- Serializes enums (`Input.SPEECH` -> `"speech"`)
- `verb` is always emitted, also with FastAPI's `response_model_exclude_unset=True`.
  Do **not** use `exclude_defaults` / `response_model_exclude_defaults`: it drops
  `verb` and jambonz rejects the response.
- Scalars are strict: `Pause(length="5")` or `Gather(bargein="yes")` is an error,
  not silently coerced. Assignments are validated too (`say.text = None` raises);
  `model_copy(update=...)` is not validated by pydantic, so build a new verb instead.
- `extra_fields={...}` adds wire fields the SDK does not model yet. Such JSON does
  not parse back into the strict model (unknown keys are rejected); it is the one
  exception to the dump/parse round trip.
- `RawVerb.of("name", **params)` sends a verb exactly as given. Pass nested verbs
  in its params as plain dicts: a `Say(...)` value keeps its `"verb"` key, which
  jambonz rejects inside another verb.

When you build the list before returning it, annotate it: mypy infers
`[Say(...), Hangup()]` as `list[VerbModel]`, which is not a `JambonzResponse`.

```python
verbs: list[Verb] = [Say(text="Hi")]
verbs.append(Hangup())
```

```python
# Works with any framework
to_json([Say(text="Hi"), Hangup()])  # -> bytes
```

## Incoming: Parsing webhooks

Typed models for what jambonz POSTs to your app live in `jambonz.payloads` (also
re-exported from `jambonz`). They are plain pydantic models for **reading**:

- They are lenient on purpose. Every field is optional (`X | None`), because jambonz
  adds fields and some hooks are sparse. A new field never makes parsing fail.
- Field names are snake_case, exactly as jambonz sends them (`call_sid`, `dial_call_status`).
  The only alias is `from` -> `from_`. The websocket frames (listen, conference listen)
  are camelCase and have their own models.
- Enums are open: `call.direction` is typed `CallDirection | str`. Compare with the
  plain strings (`"inbound"`, `"completed"`); an unknown new value arrives as a `str`
  and does not raise.
- Keys the model does not declare are kept in `model_extra` (and survive a round trip),
  e.g. your own user metadata on a `listen` websocket.
- Ids (`call_sid`, `sbc_callid`...) are `str`, never `UUID`: `sbc_callid` is not a UUID
  and `call_id` is a SIP Call-ID.

```python
result = GatherResult.model_validate(body)
result.model_extra          # {} when every key was modelled, else the unknown keys
```

Most hooks send the call envelope (`CallInfo`: `call_sid`, `from_`, `to`, `direction`,
`call_status`...) plus the verb's own result. Two hooks are **sparse** and are not
`CallInfo`: `EnqueueWait` and `SipReferEvent`.

### New call

```python
from jambonz import CallWebhook, JambonzResponse, Say

@app.post("/incoming-call")
def handle(call: CallWebhook) -> JambonzResponse:
    print(call.from_)       # caller number
    print(call.to)          # called number
    print(call.direction)   # "inbound" (CallDirection | str)
    print(call.call_sid)    # str
    return [Say(text="Hello!")]
```

### Call status

```python
from jambonz import CallStatusEvent

@app.post("/call-status")
def handle(event: CallStatusEvent):
    print(event.call_status)  # "completed" (CallStatusValue | str)
    print(event.duration)     # seconds, only when completed
```

### Gather result

```python
from jambonz import GatherResult

@app.post("/gather-result")
def handle(result: GatherResult) -> JambonzResponse:
    if result.reason == "speechDetected":
        print(result.transcript)   # best transcript, or None
        print(result.speech.alternatives[0].confidence)  # speech may be None: check it
    elif result.reason == "dtmfDetected":
        print(result.digits)       # without the finishOnKey
    else:
        print(result.reason)       # "timeout", "error", "stt-low-confidence", or a new value
```

`reason` is `GatherReason | str`, so a type checker needs the comparison above before
it narrows. A `timeout` has no `digits`, `speech` or `details`. The same model covers
the `config.bargeIn` actionHook.

### Dial result

```python
from jambonz import DialResult

@app.post("/dial-result")
def handle(result: DialResult):
    print(result.dial_call_status)  # "completed", "busy", "no-answer", "failed"...
    print(result.dial_sip_status)   # 200, 486 (busy), 487 (no answer)
    print(result.dial_call_sid)
```

The dial `dtmfHook` sends `DialDtmfEvent` (`dtmf="*2"`); its envelope is the dialed
leg, so `call_sid` is the child's and `parent_call_sid` is the caller's.

### Answering machine detection

```python
from jambonz import AmdEvent

@app.post("/amd")
def handle(event: AmdEvent):
    # several events per call, e.g. amd_no_speech_detected and then amd_stopped
    if event.type == "amd_machine_detected":
        print(event.greeting, event.language)
```

The key is `type` (not `event` or `amd_type`, which only dial.md mentions).

### Conference

```python
from jambonz import ConferenceStatusEvent

@app.post("/conference-status")
def handle(event: ConferenceStatusEvent):
    print(event.event)           # start, end, join, leave, start-talking, stop-talking
    print(event.conference_sid)  # "conf:<account_sid>:<name>"
    print(event.members)         # can be -1 on a kicked leave
    print(event.duration)        # the conference's age as a float, not call seconds
```

`ConferenceResult` (actionHook) and `ConferenceWait` (waitHook) carry only the envelope.
`end-talking` from the docs is never sent; `stop-talking` is.

### Queues

```python
from jambonz import DequeueResult, EnqueueResult, EnqueueWait

def on_enqueue_wait(wait: EnqueueWait):      # waitHook, sparse: not a CallInfo
    print(wait.queue_size, wait.queue_position, wait.queue_time)

def on_enqueue_done(result: EnqueueResult):  # actionHook
    print(result.queue_result)               # "bridged", "leave", "hangup"
    print(result.queue_time)                 # no queue_size/queue_position here

def on_dequeue(result: DequeueResult):       # jambonz does not wait for the answer
    print(result.dequeue_result)             # "complete", "timeout"
```

### SIP transfer

```python
from jambonz import SipReferEvent, SipReferResult, SipRequestResult

def on_refer_event(event: SipReferEvent):    # sparse: {event, call_status}
    print(event.event)                       # "transfer-status"
    print(event.call_status)                 # int, the SIP code from the NOTIFY (100, 200)

def on_refer_done(result: SipReferResult):
    print(result.refer_status, result.final_referred_call_status)

def on_request_done(result: SipRequestResult):
    print(result.sip_status)  # the response to the in-dialog request: trust this, not `result`
```

Overloaded keys: `call_status` is an int in the `sip:refer` eventHook, and `sip_status`
and `sip_reason` in `sip:request` describe the in-dialog response, not the call.

### Other hooks

| Hook | Model |
|---|---|
| `play` actionHook | `PlayResult` (`reason`, `playback_seconds`, `playback_milliseconds`) |
| `listen` actionHook | `ListenResult` (`dial_call_duration`, `digits` = only the finish key) |
| `listen` websocket, first frame | `ListenMetadata` (camelCase; your metadata keys are in `model_extra`) |
| `conference.listen` websocket events | `ConferenceListenEvent` (camelCase) |
| any listen frame | `parse_listen_message(json.loads(text))` |
| `transfer` actionHook | `TransferResult` |
| dial `onHoldHook`, `referHook` | `DialHoldEvent`, `DialReferEvent` |
| gather `partialResultHook` | `GatherPartialResult` |

Note that `play` with a broken URL still reports `playCompleted` with zero playback
on jambonz.cloud, and `play` errors such as an empty URL call no actionHook at all.

If a hook has no model (`dialogflow`, `transcribe`, `agent` events...), read the raw
JSON, or validate it with `CallInfo` and read the rest from `model_extra`.

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
    # jambonz adds the invocation id and type itself (Ultravox-style result).
    return ToolResult(result="done")
```

For vendors that expect their own envelope (e.g. OpenAI realtime), send it as
extra keys and no `result`; jambonz passes a body with a `type` through untouched:

```python
return ToolResult.model_validate({"type": "conversation.item.create", "item": {...}})
```
