from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import MISSING, StrictBool, StrictInt

from jambonz.verbs._base import VerbModel
from jambonz.verbs.shared import Synthesizer


class Say(VerbModel):
    """Speak text with text-to-speech.

    ``text`` is optional on the wire (an empty ``say`` is valid with ``stream=True``);
    a list of strings is spoken in sequence.
    """

    verb: Literal["say"] = "say"
    text: str | Sequence[str] | MISSING = MISSING
    instructions: str | MISSING = MISSING
    stream: StrictBool | MISSING = MISSING
    loop: StrictInt | str | MISSING = MISSING
    synthesizer: Synthesizer | MISSING = MISSING
    early_media: StrictBool | MISSING = MISSING
    disable_tts_cache: StrictBool | MISSING = MISSING
    close_stream_on_empty: StrictBool | MISSING = MISSING
