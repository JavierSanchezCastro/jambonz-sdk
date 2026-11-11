from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawVerb(BaseModel):
    """Escape hatch: a verb sent to jambonz exactly as given.

    Build it with ``RawVerb.of("name", **params)``. Parameter keys are wire keys
    (no camelCase conversion) and ``None`` values are sent as ``null``. Any verb
    name not modelled by this SDK parses as ``RawVerb`` too.

    Values are dumped as given: a strict verb used as a value keeps its ``"verb"``
    key (``RawVerb.of("gather", say=Say(text="x"))`` sends ``say.verb``, which
    jambonz rejects in nested verbs). Pass nested verbs as plain dicts.

    The parameters are the model's extra fields (``extra="allow"``), so the wire
    shape ``{"verb": name, **params}`` needs no custom serialization.
    """

    model_config = ConfigDict(extra="allow")

    verb: str = Field(min_length=1)

    @classmethod
    def of(cls, verb: str, /, **params: Any) -> RawVerb:
        if "verb" in params:
            raise ValueError("params cannot contain 'verb'; pass the name as first argument")
        return cls.model_validate({"verb": verb, **params})

    @property
    def params(self) -> dict[str, Any]:
        """The verb's parameters (everything except ``verb``)."""
        return dict(self.__pydantic_extra__ or {})
