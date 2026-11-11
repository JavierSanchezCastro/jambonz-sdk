from jambonz.models._base import Sid, _JambonzModel


class PhoneNumber(_JambonzModel):
    """https://docs.jambonz.org/reference/rest-platform-management/phone-numbers/list-phone-numbers"""

    phone_number_sid: Sid | None = None
    number: str = ""
    voip_carrier_sid: Sid | None = None
    account_sid: Sid | None = None
    application_sid: Sid | None = None
