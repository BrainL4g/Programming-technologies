from typing import List, Optional, Annotated
from pydantic import BaseModel, ConfigDict, Field


class FeatureResponse(BaseModel):
    name: str
    unit: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StorelinkResponse(BaseModel):
    storename: str
    price: float
    url: str

    model_config = ConfigDict(from_attributes=True)


class FavoriteProductResponse(BaseModel):
    id: int
    name: str
    description: str
    brand: str

    # features: Annotated[List[FeatureResponse], Field(default_factory=list)]
    # storelinks: Annotated[List[StorelinkResponse], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)
