import pytest
from pydantic import ValidationError

from app.schemas import LeadCreate


def test_valid_enquiry_accepts_international_phone() -> None:
    lead = LeadCreate(
        full_name="Aarush",
        phone="+91 98765 43210",
        preferred_contact="whatsapp",
    )
    assert lead.phone == "+91 98765 43210"


def test_invalid_phone_is_rejected() -> None:
    with pytest.raises(ValidationError):
        LeadCreate(full_name="Aarush", phone="call-me-now")


def test_email_contact_requires_email_address() -> None:
    with pytest.raises(ValidationError):
        LeadCreate(
            full_name="Aarush",
            phone="+91 98765 43210",
            preferred_contact="email",
        )


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValidationError):
        LeadCreate(
            full_name="Aarush",
            phone="+91 98765 43210",
            email="not-an-email",
        )
