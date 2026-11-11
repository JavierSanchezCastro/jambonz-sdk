"""Types shared by verbs and payloads."""

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import MISSING

from jambonz._wire import WireModel

__all__ = [
    "MISSING",
    "Auth",
    "ConferenceStatusEventName",
    "Hook",
    "HookSpec",
    "JambonzWarning",
    "MixType",
]

ConferenceStatusEventName: TypeAlias = Literal[
    "start", "end", "join", "leave", "start-talking", "stop-talking"
]
"""Conference status event names: what ``conference.status_events`` accepts and
what the statusHook's ``event`` carries.

Verified live (2026-11-10): jambonz sends only these six. Any other name is
dropped silently (``end-talking``, ``START``, ``foo``...), and a list with only
unknown names means no events at all. The docs' ``end-talking`` is a typo:
``conference.js`` has listed ``stop-talking`` since its first version (2020).
Verbs use it closed; payloads use it open (``ConferenceStatusEventName | str``)."""

MixType: TypeAlias = Literal["mono", "stereo", "mixed"]
"""Audio channel layout of a listen/stream websocket (``mixType``). Closed in the
``listen`` verb; open (``MixType | str``) in the websocket metadata frame."""


class JambonzWarning(UserWarning):
    """Valid for jambonz but probably not what you meant (e.g. outside a documented
    range). Silence with ``warnings.filterwarnings("ignore", category=JambonzWarning)``."""


class Auth(WireModel):
    """Username and password (HTTP basic auth for hooks, SIP digest for targets)."""

    username: str
    password: str


class HookSpec(WireModel):
    """A webhook reference with options. A plain ``str`` URL is also a valid ``Hook``."""

    url: str
    method: Literal["GET", "POST"] | MISSING = MISSING
    basic_auth: Auth | MISSING = MISSING  # wire: basicAuth
    """Per-hook credentials, as in jambonz's schema. Caveat: feature-server builds
    the Authorization header from the *application's* hook credentials and does
    not read them from a per-verb hook, so this may not be honoured."""


Hook: TypeAlias = str | HookSpec
"""Where jambonz should send a request: a URL/path string or a ``HookSpec``."""
