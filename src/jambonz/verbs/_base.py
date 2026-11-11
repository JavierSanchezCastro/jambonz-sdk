"""Base class for verbs and the marker for verbs nested inside another verb."""

from __future__ import annotations

from typing import Annotated, Any, TypeVar, get_args

from pydantic import MISSING, GetJsonSchemaHandler, SerializerFunctionWrapHandler, WrapSerializer
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from jambonz._wire import WireModel


class VerbModel(WireModel):
    """Base of every strict jambonz verb.

    Subclasses declare ``verb: Literal["<name>"] = "<name>"``. The literal is the
    discriminator of the ``Verb`` union and is always emitted for top-level verbs,
    also under ``model_dump(exclude_unset=True)`` and FastAPI's
    ``response_model_exclude_unset=True`` (``verb`` is marked as set on creation).

    Not supported: ``exclude_defaults=True`` drops ``verb`` (it equals its
    default) and jambonz rejects the verb. Do not use ``exclude_defaults`` or
    ``response_model_exclude_defaults`` with verbs.
    """

    id: str | MISSING = MISSING

    def model_post_init(self, context: Any, /) -> None:
        self.__pydantic_fields_set__.add("verb")


def _drop_verb(value: Any, handler: SerializerFunctionWrapHandler) -> Any:
    """Let pydantic dump the verb as usual, then drop its ``"verb"`` key."""
    data = handler(value)
    if isinstance(data, dict):
        data.pop("verb", None)
    return data


def _model_for_ref(schema_ref: object) -> type[VerbModel] | None:
    """The verb class behind a pydantic core ``schema_ref`` (``module.Qualname:id``)."""
    pending: list[type[VerbModel]] = [VerbModel]
    while pending:
        cls = pending.pop()
        if schema_ref == f"{cls.__module__}.{cls.__qualname__}:{id(cls)}":
            return cls
        pending.extend(cls.__subclasses__())
    return None


class _NoVerbInSchema:
    """``Annotated`` marker: the field's OUTPUT JSON schema is the verb's without ``verb``.

    Needed because ``WrapSerializer(_drop_verb)`` returns ``Any``, which pydantic
    would publish as an empty schema. Only affects documentation (FastAPI's
    OpenAPI), never what is sent to jambonz.
    """

    def __get_pydantic_json_schema__(
        self, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        if handler.mode != "serialization":
            return handler(core_schema)  # input: same as the verb itself
        # Ask for the verb's own schema, without our wrap serializer.
        plain = {k: v for k, v in core_schema.items() if k != "serialization"}
        ref = handler(plain)
        try:
            target = handler.resolve_ref_schema(ref)
        except LookupError:
            # The verb's definition is not generated yet (it comes later in the
            # schema's definitions, e.g. ``dial.listen`` inside the ``Verb`` union):
            # generate it now from the model's own core schema, then resolve.
            model = _model_for_ref(core_schema.get("schema_ref"))
            if model is None:
                return ref  # documents ``verb`` too; never affects the wire
            # As a definition, so pydantic stores it under its ref.
            handler(
                {
                    "type": "definitions",
                    "schema": {"type": "any"},
                    "definitions": [model.__pydantic_core_schema__],
                }
            )
            target = handler.resolve_ref_schema(ref)
        nested = dict(target)
        props = target.get("properties", {})
        nested["properties"] = {k: v for k, v in props.items() if k != "verb"}
        if "required" in target:
            nested["required"] = [r for r in target["required"] if r != "verb"]
            if not nested["required"]:
                del nested["required"]
        return nested


V = TypeVar("V", bound=VerbModel)

Nested = Annotated[V, WrapSerializer(_drop_verb), _NoVerbInSchema()]
"""A verb nested inside another verb: serialized without ``"verb"``.

    say: Nested[Say] | MISSING = MISSING
    dub: list[Nested[Dub]] | MISSING = MISSING

jambonz rejects ``"verb"`` inside nested verbs (``gather.say``, ``gather.play``,
``dial.dub``, ...): no verb spec has such a property, and feature-server's
``validateVerb`` throws ``unknown property verb``. The same instance still emits
``"verb"`` when used at the top level.

A plain ``TypeVar`` alias on purpose: a PEP 695 ``type Nested[V] = ...`` alias is a
SyntaxError before Python 3.12, and pydantic stores named aliases as their own JSON
schema definition, which breaks ``_NoVerbInSchema`` (``LookupError``).
"""


def literal_value(model: type[VerbModel]) -> str:
    """The wire name of a verb class, read from its ``verb`` Literal annotation."""
    field = model.model_fields["verb"]
    (value,) = get_args(field.annotation)
    if not isinstance(value, str):
        raise TypeError(f"{model.__name__}.verb must be a str Literal")
    return value
