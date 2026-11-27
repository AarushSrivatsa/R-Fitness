from datetime import datetime
from decimal import Decimal
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=32)
    email: EmailStr | None = Field(default=None, max_length=254)
    fitness_goal: str | None = Field(default=None, max_length=120)
    preferred_contact: Literal["whatsapp", "phone", "email"] = "whatsapp"
    message: str | None = Field(default=None, max_length=2000)

    @field_validator("full_name")
    @classmethod
    def strip_required_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = value.strip()
        digits = re.sub(r"\D", "", value)
        if not re.fullmatch(r"[0-9+().\-\s]{7,32}", value) or not 7 <= len(digits) <= 15:
            raise ValueError("Enter a valid phone number, including country code if needed.")
        return value

    @model_validator(mode="after")
    def require_email_for_email_contact(self):
        if self.preferred_contact == "email" and self.email is None:
            raise ValueError("An email address is required when email is the preferred contact method.")
        return self


class LeadOut(ORMModel):
    id: int
    full_name: str
    phone: str
    email: EmailStr | None
    fitness_goal: str | None
    preferred_contact: str
    message: str | None
    status: str
    created_at: datetime


class LeadStatusUpdate(BaseModel):
    status: Literal["new", "contacted", "converted", "closed"]


class PlanCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None
    duration_days: int | None = Field(default=None, ge=1, le=3650)
    price_amount: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    price_label: str = Field(default="Contact for pricing", max_length=80)
    features: list[str] = Field(default_factory=list, max_length=20)
    display_order: int = 0
    is_active: bool = True


class PlanUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    duration_days: int | None = Field(default=None, ge=1, le=3650)
    price_amount: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    price_label: str | None = Field(default=None, max_length=80)
    features: list[str] | None = Field(default=None, max_length=20)
    display_order: int | None = None
    is_active: bool | None = None


class PlanOut(ORMModel):
    id: int
    title: str
    description: str | None
    duration_days: int | None
    price_amount: Decimal | None
    price_label: str
    features: list[str]
    display_order: int
    is_active: bool
