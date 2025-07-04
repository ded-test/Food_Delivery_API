from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing import Optional, List
import hashlib
import secrets


class UserAddressBase(BaseModel):
    street: str
    house_number: str
    apartment: str
    city: str
    country: str

    @field_validator("street", "city", "country")
    @classmethod
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressUpdate(BaseModel):
    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    @field_validator("street", "city", "country")
    @classmethod
    def validate_non_empty_strings_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("The field cannot be empty")
        return v.strip() if v else v


class UserAddressResponse(UserAddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    number: str

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError("The name must contain at least 2 characters.")
        return v.strip().title()

    @field_validator("number")
    @classmethod
    def validate_phone_number(cls, v):
        cleaned = "".join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError("The phone number must contain at least 10 digits.")
        return v


class UserCreate(UserBase):
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("The password must contain at least 8 characters.")
        if not any(c.isupper() for c in v):
            raise ValueError("The password must contain at least one capital letter")
        if not any(c.islower() for c in v):
            raise ValueError("The password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in v):
            raise ValueError("The password must contain at least one digit.")
        return v

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self

    def create_password_hash(self) -> tuple[str, str]:
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", self.password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return salt, password_hash


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    number: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names_if_provided(cls, v):
        if v is not None and (not v or len(v.strip()) < 2):
            raise ValueError("The name must contain at least 2 characters.")
        return v.strip().title() if v else v

    @field_validator("number")
    @classmethod
    def validate_phone_number_if_provided(cls, v):
        if v is not None:
            cleaned = "".join(filter(str.isdigit, v))
            if len(cleaned) < 10:
                raise ValueError("The phone number must contain at least 10 digits.")
        return v


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("The password must contain at least 8 characters.")
        if not any(c.isupper() for c in v):
            raise ValueError("The password must contain at least one capital letter")
        if not any(c.islower() for c in v):
            raise ValueError("The password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in v):
            raise ValueError("The password must contain at least one digit.")
        return v

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords don't match")
        return self

    def create_password_hash(self, password: str) -> tuple[str, str]:
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return salt, password_hash


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserWithAddresses(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    addresses: List[UserAddressResponse] = []


class UserLogin(BaseModel):
    number: str
    password: str

    @field_validator("number")
    @classmethod
    def validate_phone_number(cls, v):
        cleaned = "".join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError("The phone number must contain at least 10 digits.")
        return v
