from jambonz.models.accounts import Account
from jambonz.resources._base import SyncResource, AsyncResource


class Accounts(SyncResource[Account]):
    _model = Account
    _path = "Accounts"


class AsyncAccounts(AsyncResource[Account]):
    _model = Account
    _path = "Accounts"
