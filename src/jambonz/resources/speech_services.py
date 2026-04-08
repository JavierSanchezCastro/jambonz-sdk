from jambonz.models.speech_services import SpeechService
from jambonz.resources._base import SyncResource, AsyncResource


class SpeechServices(SyncResource[SpeechService]):
    _model = SpeechService
    _path = "Accounts/{account_sid}/SpeechCredentials"


class AsyncSpeechServices(AsyncResource[SpeechService]):
    _model = SpeechService
    _path = "Accounts/{account_sid}/SpeechCredentials"
