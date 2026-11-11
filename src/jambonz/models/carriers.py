from enum import Enum

from jambonz.models._base import Sid, _JambonzModel


class TrunkType(str, Enum):
    STATIC_IP = "static_ip"
    AUTH = "auth"
    REGISTRATION = "reg"


class Carrier(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/carriers/list-voip-carriers"""

    service_provider_sid: Sid | None = None
    name: str = ""
    description: str | None = None
    account_sid: Sid | None = None
    application_sid: Sid | None = None
    e164_leading_plus: bool = False
    requires_register: bool = False
    register_username: str | None = None
    register_sip_realm: str | None = None
    register_password: str | None = None
    tech_prefix: str | None = None
    diversion: str | None = None
    is_active: bool = True
    smpp_system_id: str | None = None
    smpp_password: str | None = None
    smpp_inbound_system_id: str | None = None
    smpp_inbound_password: str | None = None
    smpp_enquire_link_interval: int = 0
    trunk_type: TrunkType | None = None
    inbound_auth_username: str | None = None
    inbound_auth_password: str | None = None
    voip_carrier_sid: Sid | None = None


class SipGateway(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/sip-gateways/list-sip-gateways"""

    sip_gateway_sid: Sid | None = None
    ipv4: str | None = None
    port: int = 5060
    netmask: int = 32
    voip_carrier_sid: Sid | None = None
    inbound: bool = False
    outbound: bool = False
