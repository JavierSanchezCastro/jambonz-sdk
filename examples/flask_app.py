"""Same simple greeting but using Flask instead of FastAPI."""
from flask import Flask, Response, request

from jambonz import CallWebhook, Hangup, Pause, Say, to_json

app = Flask(__name__)


@app.post("/jambonz-call")
def handle_call() -> Response:
    call = CallWebhook.model_validate(request.get_json())
    print(f"Call from {call.from_} to {call.to}")

    body = to_json([
        Say(text="Hello! Welcome to our service."),
        Pause(length=1),
        Say(text="Goodbye!"),
        Hangup(),
    ])
    return Response(body, content_type="application/json")
