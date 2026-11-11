from jambonz.models.carriers import SipGateway
from jambonz.resources._base import AsyncResource, SyncResource


class Gateways(SyncResource[SipGateway]):
    _model = SipGateway
    _path = "SipGateways"


class AsyncGateways(AsyncResource[SipGateway]):
    _model = SipGateway
    _path = "SipGateways"
