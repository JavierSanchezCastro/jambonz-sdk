"""Gather speech input, echo it back, and hang up."""
from fastapi import FastAPI

from jambonz import (
    CallWebhook,
    GatherResult,
    JambonzResponse,
    Say,
    Gather,
    Hangup,
    Input,
)

app = FastAPI()


@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    print(f"Call from {call.from_} to {call.to}")
    return [
        Say(text="Please say something and I will repeat it back to you."),
        Gather(input=[Input.SPEECH], action_hook="/gather-result", timeout=10),
    ]


@app.post("/gather-result")
def handle_gather(result: GatherResult) -> JambonzResponse:
    if result.transcript:
        print(f"User said: {result.transcript}")
        return [
            Say(text=f"You said: {result.transcript}. Goodbye!"),
            Hangup(),
        ]

    print(f"Gather ended: {result.reason}")
    return [
        Say(text="I didn't catch that. Goodbye!"),
        Hangup(),
    ]
