import json

from jambonz import (
    JambonzResponse,
    Say,
    Gather,
    Hangup,
    Play,
    Pause,
    LLM,
    Dial,
    Redirect,
    Input,
    Synthesizer,
    Recognizer,
)


class TestVerbSerialization:
    def test_say_basic(self):
        s = Say(text="Hello")
        d = s.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d == {"verb": "say", "text": "Hello"}

    def test_say_with_synthesizer(self):
        s = Say(text="Hola", synthesizer=Synthesizer(vendor="elevenlabs", language="es"))
        d = s.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d["synthesizer"]["vendor"] == "elevenlabs"
        assert d["synthesizer"]["language"] == "es"

    def test_gather_aliases(self):
        g = Gather(input=[Input.SPEECH], action_hook="/resp", num_digits=4)
        d = g.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d["actionHook"] == "/resp"
        assert d["numDigits"] == 4
        assert "action_hook" not in d

    def test_gather_enum_serializes_to_string(self):
        g = Gather(input=[Input.SPEECH, Input.DIGITS])
        d = g.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d["input"] == ["speech", "digits"]

    def test_gather_nested_say(self):
        g = Gather(
            input=[Input.SPEECH],
            action_hook="/resp",
            say=Say(text="Say something"),
        )
        d = g.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d["say"]["text"] == "Say something"

    def test_hangup(self):
        assert Hangup().model_dump(mode="json") == {"verb": "hangup"}

    def test_play(self):
        p = Play(url="https://example.com/audio.mp3")
        d = p.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d == {"verb": "play", "url": "https://example.com/audio.mp3"}

    def test_pause(self):
        p = Pause(length=2.5)
        d = p.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d == {"verb": "pause", "length": 2.5}

    def test_llm(self):
        l = LLM(vendor="elevenlabs", auth={"agent_id": "abc"}, llm_options={}, action_hook="/done")
        d = l.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d["vendor"] == "elevenlabs"
        assert d["auth"]["agentId"] == "abc"
        assert d["llmOptions"] == {}
        assert d["actionHook"] == "/done"

    def test_redirect(self):
        r = Redirect(action_hook="/new-path")
        d = r.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert d == {"verb": "redirect", "actionHook": "/new-path"}

    def test_dial(self):
        d = Dial(
            action_hook="/dial-done",
            caller_id="+34931228497",
            target=[{"type": "phone", "number": "+34600000000"}],
        )
        dump = d.model_dump(mode="json", by_alias=True, exclude_none=True)
        assert dump["callerId"] == "+34931228497"
        assert dump["target"][0]["number"] == "+34600000000"


class TestJambonzResponse:
    def test_construct_from_list(self):
        r = JambonzResponse([Say(text="Hi"), Hangup()])
        assert len(r.root) == 2

    def test_serialization_excludes_none(self):
        r = JambonzResponse([Say(text="Hi"), Hangup()])
        data = r.model_dump()
        for verb in data:
            assert None not in verb.values()

    def test_serialization_uses_aliases(self):
        r = JambonzResponse([Gather(input=[Input.SPEECH], action_hook="/resp")])
        data = r.model_dump()
        assert data[0]["actionHook"] == "/resp"
        assert "action_hook" not in data[0]

    def test_serialization_enums_as_strings(self):
        r = JambonzResponse([Gather(input=[Input.SPEECH])])
        data = r.model_dump()
        assert data[0]["input"] == ["speech"]

    def test_json_serializable(self):
        r = JambonzResponse([Say(text="Hi"), Gather(input=[Input.SPEECH], action_hook="/r"), Hangup()])
        serialized = json.dumps(r.model_dump())
        parsed = json.loads(serialized)
        assert len(parsed) == 3
        assert parsed[0]["verb"] == "say"

    def test_model_dump_json(self):
        r = JambonzResponse([Say(text="Hi"), Hangup()])
        parsed = json.loads(r.model_dump_json())
        assert parsed[0] == {"verb": "say", "text": "Hi"}

    def test_empty_response(self):
        r = JambonzResponse([])
        assert r.model_dump() == []
