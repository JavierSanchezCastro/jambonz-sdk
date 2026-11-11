"""Payloads of ``conference``'s hooks (statusHook, actionHook, waitHook)."""

from __future__ import annotations

from jambonz.payloads.call import CallInfo
from jambonz.types import ConferenceStatusEventName


class ConferenceStatusEvent(CallInfo):
    """Body of ``conference``'s statusHook (live, official schema ``conference-status``).

    Fires once per event listed in the verb's ``statusEvents``; the response is
    ignored. Quirks seen live:

    * ``members`` can be ``-1`` (a kicked member, or a second ``leave``), and
      ``leave`` can arrive twice for the same call;
    * the envelope ``duration`` is the conference's age in seconds as a float
      (e.g. ``1.69``). On ``leave``/``end`` after the call completed, jambonz has
      sent an int alongside ``call_status`` ``completed`` and
      ``call_termination_by``, which looks like call seconds: do not rely on its
      meaning;
    * carries ``b3`` (trace header);
    * the docs' camelCase ``conferenceSid``/``friendlyName`` were never seen
      live (snake_case only); if sent they would land in ``model_extra``.
    """

    event: ConferenceStatusEventName | str
    """Open enum; the docs' ``end-talking`` is never sent (``stop-talking`` is, live)."""
    conference_sid: str
    """``conf:<account_sid>:<name>`` (live, always present)."""
    friendly_name: str | None = None
    """The conference name given to the verb."""
    members: int | None = None
    """Member count after the event; can be ``-1`` (live)."""
    time: str | None = None
    """ISO-8601 timestamp of the event, kept as a string."""


class ConferenceResult(CallInfo):
    """Body of ``conference``'s actionHook (the caller left the conference).

    Only the call envelope (live, official schema ``conference``). May fire twice.
    """


class ConferenceWait(CallInfo):
    """Body of ``conference``'s waitHook (live, official schema ``conference-wait``).

    The call envelope in its ``call_hook`` form: ``local_sip_address``,
    ``public_ip``, ``has_recording`` and ``caller_name``; no ``fs_*`` or
    ``api_base_url``. Reply with verbs to play while waiting for the conference
    to start.
    """
