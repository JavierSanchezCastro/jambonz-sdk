"""Strict base for everything we *send* to jambonz (verbs and their parts).

Wire rules live in the model config, not in custom serialization code:

* field names are snake_case in Python and camelCase on the wire
  (``alias_generator=to_camel`` + ``serialize_by_alias=True``);
* unknown fields are rejected (``extra="forbid"``), like jambonz's own validator;
* optional fields are typed ``T | MISSING = MISSING``; pydantic omits a field
  whose value is ``MISSING`` when dumping, so nothing unset ever reaches the wire;
* scalar fields use ``StrictBool``/``StrictInt``/``StrictFloat``, so ``"5"`` or
  ``True`` is rejected for a number instead of being silently coerced;
* assignments are validated (``validate_assignment=True``).

The only custom serialization is the ``extra_fields`` merge below.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Annotated, Any

from pydantic import (
    MISSING,
    BaseModel,
    ConfigDict,
    Field,
    GetJsonSchemaHandler,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer,
)
from pydantic.alias_generators import to_camel
from pydantic.json_schema import JsonSchemaValue, SkipJsonSchema
from pydantic_core import CoreSchema, to_jsonable_python


class WireModel(BaseModel):
    """Strict, camelCase, self-serializing model.

    ``extra_fields`` is the escape hatch for wire fields this SDK does not model
    yet. Its keys are wire keys (no camelCase conversion), its values go out as
    given (``None`` becomes ``null``) and it wins over a modelled field with the
    same wire key. The ``extra_fields`` key itself is never emitted.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="forbid",
        # Re-validate on attribute assignment, so ``say.text = None`` raises like
        # ``Say(text=None)``. ``model_copy(update=...)`` still skips validation
        # (pydantic behaviour); build a new instance instead.
        validate_assignment=True,
    )

    extra_fields: Annotated[dict[str, Any] | MISSING, SkipJsonSchema()] = Field(
        default=MISSING, exclude=True, validation_alias="extra_fields"
    )

    def __repr_args__(self) -> Iterable[tuple[str | None, Any]]:
        return [(k, v) for k, v in super().__repr_args__() if v is not MISSING]

    @field_validator("extra_fields")
    @classmethod
    def _no_verb_in_extra_fields(cls, value: dict[str, Any]) -> dict[str, Any]:
        if "verb" in value:
            raise ValueError("'verb' cannot be set through extra_fields; use RawVerb instead")
        return value

    @model_serializer(mode="wrap")
    def _merge_extra_fields(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> dict[str, Any]:
        data: dict[str, Any] = handler(self)
        if self.extra_fields is not MISSING and self.extra_fields:
            extra = self.extra_fields
            data.update(to_jsonable_python(extra) if info.mode_is_json() else extra)
        return data

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # The wrap serializer above is annotated ``-> dict[str, Any]``; left alone,
        # pydantic would publish that as the serialization-mode JSON schema
        # (``{"type": "object"}``) and FastAPI's OpenAPI would lose every field.
        # The merge does not change the shape, so describe the model's own fields.
        if core_schema.get("type") == "model" and "serialization" in core_schema:
            core_schema = {k: v for k, v in core_schema.items() if k != "serialization"}
        json_schema = handler(core_schema)
        if handler.mode == "serialization":
            target = handler.resolve_ref_schema(json_schema)
            # ``extra_fields`` can add any key to the output, so the *output* schema
            # must not claim ``additionalProperties: false`` (input stays strict).
            target.pop("additionalProperties", None)
            # A top-level verb always emits ``verb`` (nested copies drop the property).
            if "verb" in target.get("properties", {}):
                required = target.setdefault("required", [])
                if "verb" not in required:
                    required.insert(0, "verb")
        return json_schema
