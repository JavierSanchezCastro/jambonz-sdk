from jambonz.models.accounts import User
from jambonz.resources._base import SyncResource, AsyncResource


class Users(SyncResource[User]):
    _model = User
    _path = "Users"


class AsyncUsers(AsyncResource[User]):
    _model = User
    _path = "Users"
