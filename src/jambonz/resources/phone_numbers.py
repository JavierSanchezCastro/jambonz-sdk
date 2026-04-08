from jambonz.models.phone_numbers import PhoneNumber
from jambonz.resources._base import SyncResource, AsyncResource


class PhoneNumbers(SyncResource[PhoneNumber]):
    _model = PhoneNumber
    _path = "PhoneNumbers"


class AsyncPhoneNumbers(AsyncResource[PhoneNumber]):
    _model = PhoneNumber
    _path = "PhoneNumbers"
