from jambonz.models._base import Sid, Webhook, _JambonzModel


class Account(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/accounts/list-accounts"""
    account_sid: Sid | None = None
    name: str | None = None
    sip_realm: str | None = None
    registration_hook: Webhook | None = None
    device_calling_application_sid: Sid | None = None
    service_provider_sid: Sid | None = None
    record_all_calls: bool = False
    record_format: str | None = None
    bucket_credential: dict | None = None


class ApiKey(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/api-keys/list-api-keys"""
    api_key_sid: Sid | None = None
    token: str | None = None
    account_sid: Sid | None = None
    service_provider_sid: Sid | None = None
    expires_at: str | None = None
    created_at: str | None = None
    last_used: str | None = None


class User(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/users/create-user"""
    user_sid: Sid | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    account_sid: Sid | None = None
    service_provider_sid: Sid | None = None
    scope: str | None = None
    is_active: bool = True
