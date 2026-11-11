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

Serialize the verb list with `to_json`:

```python
from flask import Flask, Response
from jambonz import Say, Hangup, to_json

app = Flask(__name__)

@app.post("/jambonz-call")
def handle_call():
    return Response(to_json([Say(text="Hello!"), Hangup()]), content_type="application/json")
```

## Django

```python
from django.http import HttpResponse
from jambonz import Say, Hangup, to_json

def handle_call(request):
    return HttpResponse(to_json([Say(text="Hello!"), Hangup()]), content_type="application/json")
```

## Comparison

| | FastAPI | Flask | Django |
|---|---|---|---|
| Serialization | Automatic (`-> JambonzResponse`) | `to_json(verbs)` | `to_json(verbs)` |
| Webhook parsing | Automatic (`call: CallWebhook`) | Manual (`request.get_json()`) | Manual (`json.loads(request.body)`) |
| Async | Native | Via Quart | Via async views |
