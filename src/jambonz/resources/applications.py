from jambonz.models.applications import Application
from jambonz.resources._base import SyncResource, AsyncResource


class Applications(SyncResource[Application]):
    _model = Application
    _path = "Accounts/{account_sid}/Applications"


class AsyncApplications(AsyncResource[Application]):
    _model = Application
    _path = "Accounts/{account_sid}/Applications"
