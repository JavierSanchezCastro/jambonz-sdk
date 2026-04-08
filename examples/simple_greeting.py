"""Simple greeting: answer, say hello, pause, hang up."""
from fastapi import FastAPI

from jambonz import CallWebhook, CallStatusEvent, JambonzResponse, Say, Pause, Hangup

app = FastAPI()


@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    print(f"Call from {call.from_} to {call.to}")
    return [
        Say(text="Hello! Welcome to our service."),
        Pause(length=1.0),
        Say(text="Goodbye!"),
        Hangup(),
    ]


@app.post("/jambonz-status")
def handle_status(event: CallStatusEvent):
    print(f"Status: {event.call_status} (sip {event.sip_status})")
