from jambonz.models.accounts import ApiKey
from jambonz.resources._base import SyncResource, AsyncResource


class ApiKeys(SyncResource[ApiKey]):
    _model = ApiKey
    _path = "Accounts/{account_sid}/ApiKeys"


class AsyncApiKeys(AsyncResource[ApiKey]):
    _model = ApiKey
    _path = "Accounts/{account_sid}/ApiKeys"
