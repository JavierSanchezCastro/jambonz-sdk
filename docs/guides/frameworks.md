# Framework Integration

## FastAPI

Return a list of verbs with a type hint — FastAPI handles serialization:

```python
from fastapi import FastAPI
from jambonz import CallWebhook, GatherResult, JambonzResponse, Say, Gather, Hangup, Input

app = FastAPI()

@app.post("/jambonz-call")
def handle_call(call: CallWebhook) -> JambonzResponse:
    return [
        Say(text="Hello! Say something."),
        Gather(input=[Input.SPEECH], action_hook="/speech"),
    ]

@app.post("/speech")
def handle_speech(result: GatherResult) -> JambonzResponse:
    return [
        Say(text=f"You said: {result.transcript}. Goodbye!"),
        Hangup(),
    ]
```

Run:

```bash
pip install jambonz-sdk fastapi uvicorn
uvicorn myapp:app --host 127.0.0.1 --port 8000
```

## Flask

Construct `JambonzResponse` and serialize manually:

```python
from flask import Flask, request
from jambonz import JambonzResponse, Say, Hangup

app = Flask(__name__)

@app.post("/jambonz-call")
def handle_call():
    response = JambonzResponse([Say(text="Hello!"), Hangup()])
    return app.response_class(
        response.model_dump_json(),
        content_type="application/json",
    )
```

## Django

```python
from django.http import HttpResponse
from jambonz import JambonzResponse, Say, Hangup

def handle_call(request):
    response = JambonzResponse([Say(text="Hello!"), Hangup()])
    return HttpResponse(
        response.model_dump_json(),
        content_type="application/json",
    )
```

## Comparison

| | FastAPI | Flask | Django |
|---|---|---|---|
| Serialization | Automatic (`-> JambonzResponse`) | `response.model_dump_json()` | `response.model_dump_json()` |
| Webhook parsing | Automatic (`call: CallWebhook`) | Manual (`request.get_json()`) | Manual (`json.loads(request.body)`) |
| Async | Native | Via Quart | Via async views |
