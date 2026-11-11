from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import MISSING, StrictBool, StrictFloat, StrictInt

from jambonz.types import Hook
from jambonz.verbs._base import Nested, VerbModel
from jambonz.verbs.components import ActionHookDelayAction, FillerNoise
from jambonz.verbs.play import Play
from jambonz.verbs.say import Say
from jambonz.verbs.shared import Input, Recognizer

__all__ = ["FillerNoise", "Gather", "Input"]


class Gather(VerbModel):
    """Collect DTMF digits and/or speech.

    Without ``action_hook`` jambonz simply continues with the next verb (verified
    on jambonz.cloud). ``say``/``play`` are nested prompts and are sent without a
    ``"verb"`` key. jambonz's own defaults apply to anything left unset (input
    ``["digits"]``, timeout 15 s, ``listenDuringPrompt`` true, minDigits 1,
    minBargeinWordCount 1); this model never sends them for you.
    ``action_hook_delay_action`` plays filler while ``action_hook`` is slow.
    """

    verb: Literal["gather"] = "gather"
    action_hook: Hook | MISSING = MISSING
    input: Sequence[Input | Literal["digits", "speech"]] | MISSING = MISSING
    finish_on_key: str | MISSING = MISSING
    num_digits: StrictInt | MISSING = MISSING
    min_digits: StrictInt | MISSING = MISSING
    max_digits: StrictInt | MISSING = MISSING
    inter_digit_timeout: StrictInt | StrictFloat | MISSING = MISSING
    partial_result_hook: Hook | MISSING = MISSING
    speech_timeout: StrictInt | StrictFloat | MISSING = MISSING
    listen_during_prompt: StrictBool | MISSING = MISSING
    dtmf_bargein: StrictBool | MISSING = MISSING
    bargein: StrictBool | MISSING = MISSING
    min_bargein_word_count: StrictInt | MISSING = MISSING
    timeout: StrictInt | StrictFloat | MISSING = MISSING
    recognizer: Recognizer | MISSING = MISSING
    say: Nested[Say] | MISSING = MISSING
    play: Nested[Play] | MISSING = MISSING
    filler_noise: FillerNoise | MISSING = MISSING
    action_hook_delay_action: ActionHookDelayAction | MISSING = MISSING
