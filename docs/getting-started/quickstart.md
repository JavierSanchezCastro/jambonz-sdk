# Quick Start

## REST API Client

```python
import asyncio
from jambonz import AsyncJambonzClient

async def main():
    async with AsyncJambonzClient() as client:
        # Phone numbers
        for n in await client.phone_numbers.list():
            print(f"{n.number} -> app: {n.application_sid}")

        # Carriers and gateways
        for c in await client.carriers.list():
            print(f"{c.name}")
            for gw in await client.gateways.list(voip_carrier_sid=c.voip_carrier_sid):
                print(f"  {gw.ipv4}:{gw.port}")

        # Recent calls
        for call in await client.recent_calls.list(days=7, count=5):
            print(f"{call.from_} -> {call.to} ({call.duration}s)")

asyncio.run(main())
```

Run it:

```bash
python examples/rest_client.py
```

## Webhook Server

Build a voice app that answers calls:

```python
from fastapi import FastAPI
from jambonz import CallWebhook, JambonzResponse, Say, Pause, Hangup

app = FastAPI()

@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        Say(text="Hello! Welcome to our service."),
        Pause(length=1.0),
        Say(text="Goodbye!"),
        Hangup(),
    ]
```

Run it:

```bash
uv run python -m uvicorn examples.simple_greeting:app --host 127.0.0.1 --port 8000
```

Expose it with ngrok:

```bash
ngrok http 127.0.0.1:8000
```

Then point your jambonz application's webhook to `https://your-ngrok-url/jambonz-call`.

## Speech Recognition

Collect speech input and respond:

```python
from jambonz import CallWebhook, GatherResult, JambonzResponse, Say, Gather, Hangup, Input

@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        Say(text="Please say something."),
        Gather(input=[Input.SPEECH], action_hook="/gather-result", timeout=10),
    ]

@app.post("/gather-result")
def handle_gather(result: GatherResult) -> JambonzResponse:
    return [
        Say(text=f"You said: {result.transcript}. Goodbye!"),
        Hangup(),
    ]
```

## Conversational AI

Connect to an ElevenLabs agent:

```python
from jambonz import CallWebhook, LLMResult, JambonzResponse, LLM, LLMAuth

@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        LLM(
            vendor="elevenlabs",
            auth=LLMAuth(agent_id="your-agent-id"),
            llm_options={},
            action_hook="/llm-complete",
        ),
    ]

@app.post("/llm-complete")
def handle_llm(result: LLMResult):
    print(f"Session ended: {result.completion_reason}")
```
