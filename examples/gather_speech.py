"""Gather speech input, echo it back, and hang up."""
from fastapi import FastAPI

from jambonz import (
    CallWebhook,
    Gather,
    GatherResult,
    Hangup,
    JambonzResponse,
    Recognizer,
    Say,
)

app = FastAPI()


@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    print(f"Call from {call.from_} to {call.to}")
    return [
        Gather(
            input=["speech"],
            action_hook="/gather-result",
            timeout=10,
            recognizer=Recognizer(vendor="deepgram", language="en-US"),
            say=Say(text="Please say something and I will repeat it back to you."),
        ),
        Say(text="I didn't hear anything. Goodbye!"),
        Hangup(),
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
