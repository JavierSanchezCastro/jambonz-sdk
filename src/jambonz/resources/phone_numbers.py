from jambonz.models.phone_numbers import PhoneNumber
from jambonz.resources._base import AsyncResource, SyncResource


class PhoneNumbers(SyncResource[PhoneNumber]):
    _model = PhoneNumber
    _path = "PhoneNumbers"


class AsyncPhoneNumbers(AsyncResource[PhoneNumber]):
    _model = PhoneNumber
    _path = "PhoneNumbers"
