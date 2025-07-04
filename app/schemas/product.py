from pydantic import BaseModel, field_validator
from typing import Optional


class CategoryBase(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("The category name should not be empty.")
        if len(v.strip()) < 2:
            raise ValueError("The category name must contain at least 2 characters")
        if len(v.strip()) > 100:
            raise ValueError("The category name should not exceed 100 characters")
        return v.strip()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name_if_provided(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("The category name should not be empty.")
            if len(v.strip()) < 2:
                raise ValueError("The category name must contain at least 2 characters")
            if len(v.strip()) > 100:
                raise ValueError("The category name should not exceed 100 characters")
            return v.strip()
        return v


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool = False
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("The product name should not be empty.")
        if len(v.strip()) < 2:
            raise ValueError("The product name must contain at least 2 characters")
        if len(v.strip()) > 100:
            raise ValueError("The product name should not exceed 100 characters")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if v and len(v.strip()) > 255:
            raise ValueError("The description should not exceed 255 characters")
        return v.strip() if v else v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("The price must be more than 0")
        if v > 999_999.99:
            raise ValueError("The price is too high")
        return round(v, 2)

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, v):
        if v <= 0:
            raise ValueError("The category ID must be greater than 0")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_name_if_provided(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("The product name should not be empty.")
            if len(v.strip()) < 2:
                raise ValueError("The product name must contain at least 2 characters")
            if len(v.strip()) > 100:
                raise ValueError("The product name should not exceed 100 characters")
            return v.strip()
        return v

    @field_validator("description")
    @classmethod
    def validate_description_if_provided(cls, v):
        if v is not None and len(v.strip()) > 255:
            raise ValueError("The description should not exceed 255 characters")
        return v.strip() if v else v

    @field_validator("price")
    @classmethod
    def validate_price_if_provided(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("The price must be more than 0")
            if v > 999999.99:
                raise ValueError("The price is too high")
            return round(v, 2)
        return v

    @field_validator("category_id")
    @classmethod
    def validate_category_id_if_provided(cls, v):
        if v is not None and v <= 0:
            raise ValueError("The category ID must be greater than 0")
        return v


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
