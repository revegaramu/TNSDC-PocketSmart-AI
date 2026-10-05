from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("Enter a valid email address.")
        return value


class LoginRequest(BaseModel):
    email: str
    password: str


class HomeRequest(BaseModel):
    room_type: str = Field(min_length=2, max_length=60)
    budget: float = Field(gt=0, le=100000000)
    style: str = Field(min_length=2, max_length=60)
    notes: str = Field(default="", max_length=500)


class PartyRequest(BaseModel):
    occasion: str = Field(min_length=2, max_length=80)
    budget: float = Field(gt=0, le=100000000)
    guests: int = Field(ge=1, le=10000)
    location_type: str = Field(default="Indoor", max_length=60)
    notes: str = Field(default="", max_length=500)


class JewelryRequest(BaseModel):
    occasion: str = Field(min_length=2, max_length=80)
    outfit_color: str = Field(min_length=2, max_length=60)
    budget: float = Field(gt=0, le=100000000)
    jewelry_type: str = Field(default="Any", max_length=60)
    notes: str = Field(default="", max_length=500)