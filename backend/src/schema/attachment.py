from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttachmentBase(BaseModel):
    product_id: Optional[int] = None
    category_id: Optional[int] = None


class AttachmentResponse(AttachmentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


