from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import MISSING, StrictBool, StrictInt

from jambonz.types import Hook
from jambonz.verbs._base import VerbModel


class Play(VerbModel):
    """Play one audio URL, or several in sequence."""

    verb: Literal["play"] = "play"
    url: str | Sequence[str]
    loop: StrictInt | str | MISSING = MISSING
    early_media: StrictBool | MISSING = MISSING
    seek_offset: StrictInt | str | MISSING = MISSING
    timeout_secs: StrictInt | str | MISSING = MISSING
    action_hook: Hook | MISSING = MISSING
