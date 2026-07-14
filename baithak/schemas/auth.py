from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=6, max_length=128)

    @model_validator(mode="after")
    def require_email_or_phone(self):
        email = self.email
        phone = (self.phone or "").strip() or None
        self.phone = phone
        if not email and not phone:
            raise ValueError("Provide either email or phone number")
        return self


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=1, max_length=128)

    @model_validator(mode="after")
    def require_email_or_phone(self):
        phone = (self.phone or "").strip() or None
        self.phone = phone
        if not self.email and not phone:
            raise ValueError("Provide either email or phone number")
        return self


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str | None
    phone: str | None
    registration_number: int
    early_bird_discount: bool

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
