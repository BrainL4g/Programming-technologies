from typing import Optional

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.db.models import Attachment

class AttachmentCRUD:
    async def create_attachment(self, db: AsyncSession,
                                file_url: str,
                                product_id: Optional[int] = None,
                                category_id: Optional[int] = None) -> Attachment:
        attachment = Attachment(
            file_url=file_url,
            product_id=product_id,
            category_id=category_id
        )
        db.add(attachment)
        await db.commit()
        await db.refresh(attachment)
        return attachment

    async def get_by_id(self, db: AsyncSession, attachment_id: int) -> Optional[Attachment]:
        stmt = select(Attachment).where(Attachment.id == attachment_id)
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def get_by_category_id(self, db: AsyncSession, category_id: int) -> Optional[Attachment]:
        stmt = select(Attachment).where(Attachment.category_id == category_id)
        query = await db.execute(statement=stmt)
        return query.scalar_one_or_none()

    async def delete(self, db: AsyncSession, attachment: Attachment) -> None:
        await db.delete(attachment)
        await db.commit()


AttachCrud = AttachmentCRUD()