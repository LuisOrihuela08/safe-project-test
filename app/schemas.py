from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    active: bool | None = None


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
