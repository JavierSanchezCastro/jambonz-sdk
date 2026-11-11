from jambonz.models._base import Sid, _JambonzModel


class SpeechService(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/speech-credentials/list-speech-credentials"""

    speech_credential_sid: Sid | None = None
    account_sid: Sid | None = None
    vendor: str = ""
    service_key: str | None = None
    access_key_id: str | None = None
    secret_access_key: str | None = None
    aws_region: str | None = None
    riva_server_uri: str | None = None
    last_used: str | None = None
    last_tested: str | None = None
    use_for_tts: bool = True
    use_for_stt: bool = True
    tts_tested_ok: bool | None = None
    stt_tested_ok: bool | None = None
