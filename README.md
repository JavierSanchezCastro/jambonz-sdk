# jambonz SDK for Python

A Python SDK for the [jambonz](https://jambonz.org) open-source CPaaS platform. Build voice applications, manage telephony infrastructure, and control calls programmatically.

## Install

```bash
pip install jambonz-sdk
```

## Quick start

### Environment variables

Create a `.env` file or set these environment variables:

```bash
JAMBONZ_ACCOUNT_SID=your-account-sid
JAMBONZ_API_KEY=your-api-key
```

The SDK reads them automatically. Get your credentials from the [jambonz portal](https://jambonz.cloud).

### REST API client

```python
import asyncio
from jambonz import AsyncJambonzClient

async def main():
    async with AsyncJambonzClient() as client:
        # List phone numbers
        for number in await client.phone_numbers.list():
            print(number.number)

        # List carriers and their gateways
        for carrier in await client.carriers.list():
            gateways = await client.gateways.list(voip_carrier_sid=carrier.voip_carrier_sid)
            for gw in gateways:
                print(f"  {gw.ipv4}:{gw.port}")

        # Recent call history
        for call in await client.recent_calls.list(days=7):
            print(f"{call.from_} -> {call.to} ({call.duration}s)")

asyncio.run(main())
```

### Webhook response

Build call flow instructions for incoming calls:

```python
from fastapi import FastAPI
from jambonz import CallWebhook, GatherResult, JambonzResponse, Say, Gather, Hangup, Input

app = FastAPI()

@app.post("/incoming-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        Say(text="Hello! Please say something."),
        Gather(input=[Input.SPEECH], action_hook="/handle-speech"),
    ]

@app.post("/handle-speech")
def handle_speech(result: GatherResult) -> JambonzResponse:
    return [
        Say(text=f"You said: {result.transcript}. Goodbye!"),
        Hangup(),
    ]
```

## Type checking

Optional verb fields are typed `T | MISSING` (pydantic's PEP 661 sentinel), so a
type checker rejects `Say(text=None)` and makes you narrow `say.loop is not MISSING`.
That needs a checker with sentinel support:

- **mypy >= 2.4** (older versions treat `MISSING` as `Any` and silently accept `None`)
- pyright 1.1.414 (via basedpyright 1.40.2) was checked against the typing test cases and works

## Features

- **REST API client** with sync and async support
- **Typed models** for all jambonz resources (Pydantic v2)
- **Webhook response builder** with typed verbs (Say, Gather, LLM, Dial...)
- **Webhook incoming models** for parsing call events, gather results, tool calls
- **Framework agnostic** — works with FastAPI, Flask, Django
- **Auto-config** from environment variables and `.env` files
- **Retry with backoff** on rate limits and server errors
- **Typed exceptions** for clean error handling

## Resources

| Resource | Usage |
|---|---|
| `client.accounts` | Account management |
| `client.users` | User management |
| `client.api_keys` | API key management |
| `client.carriers` | VoIP carriers (Telnyx, Twilio, etc.) |
| `client.gateways` | SIP gateways |
| `client.phone_numbers` | Phone number provisioning |
| `client.applications` | Application configuration |
| `client.speech_services` | Speech credentials (Google, AWS, ElevenLabs...) |
| `client.calls` | Active call control (create, update, hangup) |
| `client.recent_calls` | Call history |

## Documentation

Full docs at [javiersanchezcastro.github.io/jambonz-sdk](https://javiersanchezcastro.github.io/jambonz-sdk)

## License

MIT
