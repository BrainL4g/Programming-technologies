from typing import Optional, TYPE_CHECKING, Any, List

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    class CategoryResponseTree(BaseModel):
        ...
else:
    CategoryResponseTree = Any

class CategoryBase(BaseModel):
    name: str
    description: str
    parent_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    icon_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CategoryResponseTree(CategoryBase):
    id: int
    children: List['CategoryResponseTree']
    icon_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


CategoryResponseTree.model_rebuild()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
