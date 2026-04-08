from fastapi import FastAPI
from fastapi.testclient import TestClient

from jambonz import JambonzResponse, Say, Gather, Hangup, Input


app = FastAPI()


@app.post("/with-model", response_model=JambonzResponse)
def endpoint_with_model():
    return [Say(text="Hola"), Gather(input=[Input.SPEECH], action_hook="/r"), Hangup()]


@app.post("/from-list", response_model=JambonzResponse)
def endpoint_from_list():
    verbs = [Say(text="Hola")]
    verbs.append(Hangup())
    return verbs


@app.post("/type-hint")
def endpoint_type_hint() -> JambonzResponse:
    return [Say(text="Hola"), Hangup()]


@app.post("/explicit")
def endpoint_explicit():
    return JambonzResponse([Say(text="Hola"), Hangup()])


client = TestClient(app)


class TestFastAPIIntegration:
    def test_response_model_excludes_none(self):
        r = client.post("/with-model").json()
        assert r[0] == {"verb": "say", "text": "Hola"}
        assert "synthesizer" not in r[0]

    def test_response_model_uses_aliases(self):
        r = client.post("/with-model").json()
        gather = r[1]
        assert "actionHook" in gather
        assert "action_hook" not in gather

    def test_response_model_enums_as_strings(self):
        r = client.post("/with-model").json()
        assert r[1]["input"] == ["speech"]

    def test_from_list(self):
        r = client.post("/from-list").json()
        assert len(r) == 2
        assert r[0]["verb"] == "say"
        assert r[1]["verb"] == "hangup"

    def test_type_hint(self):
        r = client.post("/type-hint").json()
        assert r[0] == {"verb": "say", "text": "Hola"}
        assert "synthesizer" not in r[0]

    def test_explicit_construction(self):
        r = client.post("/explicit").json()
        assert r[0] == {"verb": "say", "text": "Hola"}
        assert "synthesizer" not in r[0]

    def test_openapi_schema_exists(self):
        schema = app.openapi()
        assert "/with-model" in schema["paths"]
