from jambonz.models.carriers import Carrier
from jambonz.resources._base import AsyncResource, SyncResource


class Carriers(SyncResource[Carrier]):
    _model = Carrier
    _path = "Accounts/{account_sid}/VoipCarriers"


class AsyncCarriers(AsyncResource[Carrier]):
    _model = Carrier
    _path = "Accounts/{account_sid}/VoipCarriers"
