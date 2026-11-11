from jambonz.models.accounts import User
from jambonz.resources._base import AsyncResource, SyncResource


class Users(SyncResource[User]):
    _model = User
    _path = "Users"


class AsyncUsers(AsyncResource[User]):
    _model = User
    _path = "Users"
