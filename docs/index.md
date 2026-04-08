# jambonz SDK for Python

A Python SDK for the [jambonz](https://jambonz.org) open-source CPaaS platform.

## What you can do

- **Manage infrastructure** — carriers, phone numbers, applications, speech services
- **Control calls** — create outbound calls, update active calls, view call history
- **Build call flows** — respond to incoming calls with typed verbs (Say, Gather, LLM, Dial...)
- **Parse webhooks** — typed models for call events, gather results, LLM tool calls

## Quick example

```python
from fastapi import FastAPI
from jambonz import CallWebhook, JambonzResponse, Say, Gather, Hangup, Input

app = FastAPI()

@app.post("/incoming-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        Say(text="Hello! Say something."),
        Gather(input=[Input.SPEECH], action_hook="/speech"),
    ]
```

## Install

```bash
pip install jambonz-sdk
```

Set your credentials:

```bash
export JAMBONZ_ACCOUNT_SID=your-account-sid
export JAMBONZ_API_KEY=your-api-key
```

Or create a `.env` file — the SDK picks it up automatically.
