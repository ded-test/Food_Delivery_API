from pydantic import BaseModel, field_validator, model_validator, ConfigDict, Field
from typing import Optional, List, Any, Self
import hashlib
import secrets


def validate_password_strength(password: str) -> str:
    """
    Checks the password strength:
        Minimum of 8 characters
        At least one capital letter
        At least one lowercase letter
        At least one digit
    """
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
    return password


def create_password_hash(password: str) -> tuple[str, str]:
    """
    Creates a secure password hash:
        Generates a random salt to protect against rainbow tables
        Uses PBKDF2 with SHA-256 and 100,000 iterations
        Returns the salt and hash separately
    """
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
    return salt, password_hash


def verify_password(password: str, stored_salt: str, stored_hash: str) -> bool:
    """Checks the password against the saved hash - recreates the hash and compares it."""
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), stored_salt.encode("utf-8"), 100000
    ).hex()
    return password_hash == stored_hash


class UserAddressBase(BaseModel):
    street: str
    house_number: str
    apartment: str
    city: str
    country: str

    @field_validator("street", "city", "country")
    @classmethod
    def validate_non_empty_strings(cls, v):
        """Automatically removes spaces at the beginning/end."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
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
            raise ValueError("Field cannot be empty")
        return v.strip() if v else v


class UserAddressResponse(UserAddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    """
    Validation:
        Names: minimum 2 characters, automatically added to the Title Case
        Phone number: minimum 10 digits (ignoring other characters)
    """

    first_name: str
    last_name: str
    number: str

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError("Name must contain at least 2 characters")
        return v.strip().title()

    @field_validator("number")
    @classmethod
    def validate_phone_number(cls, v):
        cleaned = "".join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError("Phone number must contain at least 10 digits")
        return v


class UserCreate(UserBase):
    """
    Additional validation:
        Password Strength check
        Comparing a password and its confirmation
        A method for creating a password hash
    """

    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        return validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self

    def create_password_hash(self) -> tuple[str, str]:
        return create_password_hash(self.password)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    number: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names_if_provided(cls, v):
        if v is not None and (not v or len(v.strip()) < 2):
            raise ValueError("Name must contain at least 2 characters")
        return v.strip().title() if v else v

    @field_validator("number")
    @classmethod
    def validate_phone_number_if_provided(cls, v):
        if v is not None:
            cleaned = "".join(filter(str.isdigit, v))
            if len(cleaned) < 10:
                raise ValueError("Phone number must contain at least 10 digits")
        return v


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v):
        return validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords don't match")
        return self

    def create_password_hash(self) -> tuple[str, str]:
        return create_password_hash(self.new_password)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserWithAddresses(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    addresses: List[UserAddressResponse] = []


class UserLogin(BaseModel):
    number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=1, max_length=100)

    def verify_password(self, stored_salt: str, stored_hash: str) -> bool:
        return verify_password(self.password, stored_salt, stored_hash)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
