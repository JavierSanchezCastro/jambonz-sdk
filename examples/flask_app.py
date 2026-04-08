"""Same simple greeting but using Flask instead of FastAPI."""
from flask import Flask, request

from jambonz import JambonzResponse, Say, Pause, Hangup

app = Flask(__name__)


@app.post("/jambonz-call")
def handle_call():
    data = request.get_json()
    print(f"Call from {data.get('from')} to {data.get('to')}")

    response = JambonzResponse([
        Say(text="Hello! Welcome to our service."),
        Pause(length=1.0),
        Say(text="Goodbye!"),
        Hangup(),
    ])
    return app.response_class(
        response.model_dump_json(),
        content_type="application/json",
    )
