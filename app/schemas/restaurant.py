from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None

    street: str
    house_number: str
    apartment: str
    city: str
    country: str

    @field_validator("name", "street", "house_number", "apartment", "city", "country")
    @classmethod
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    @field_validator("name", "street", "house_number", "apartment", "city", "country")
    @classmethod
    def validate_non_empty_strings_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Поле не может быть пустым")
        return v.strip() if v else v


class RestaurantResponse(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    @classmethod
    def from_orm(cls, obj):
        return cls(
            name=obj.name,
            description=obj.description,
            street=obj.street,
            house_number=obj.house_number,
            apartment=obj.apartment,
            city=obj.city,
            country=obj.country,
        )


# Additional schemes for specific cases
class RestaurantPublicInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    city: str
    country: str

    @property
    def location(self) -> str:
        return f"{self.city}, {self.country}"


class RestaurantWithFullAddress(RestaurantResponse):
    model_config = ConfigDict(from_attributes=True)

    @property
    def full_address(self) -> str:
        return f"{self.street} {self.house_number}, кв. {self.apartment}, {self.city}, {self.country}"
