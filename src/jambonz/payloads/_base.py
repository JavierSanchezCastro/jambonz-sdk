"""Flexible base for what jambonz *sends* us (hook payloads and websocket frames).

jambonz adds fields without notice (real call webhooks already carry
undocumented ones), so payload models never reject unknown input:

* unknown fields are kept (``extra="allow"``) and available in ``model_extra``;
* fields are optional (``X | None = None``) unless live payloads always carry
  them AND the official schema requires them (e.g. ``EnqueueResult.queue_sid``,
  ``ConferenceStatusEvent.event``, ``SipReferEvent.call_status``);
* SIDs are plain ``str`` (``sbc_callid`` and friends are not UUIDs);
* enums are open: fields are typed ``KnownValues | str``, so the known values
  show up in the type while a new value from jambonz still validates.

HTTP hook wire keys are snake_case and used as-is. Aliases appear only where
the wire key is not a valid Python name (the keyword ``from`` -> ``from_``) or
is camelCase on the live wire (``customerData`` -> ``customer_data``). The
listen/conference.listen websocket frames are camelCase throughout; they use
their own base (``_WsPayload`` in :mod:`jambonz.payloads.listen`) with a
camelCase alias generator.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Payload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )

    __pydantic_extra__: dict[str, Any] = Field(init=False)
