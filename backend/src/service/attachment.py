from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from src.db.models import Attachment
from src.repository.attachment import AttachCrud
from src.utils.file import save_file, delete_file
from typing import List


class AttachmentService:
    async def upload_product_image(self, db: AsyncSession, file: UploadFile, product_id: int) -> Attachment:

        file_path_str = await save_file(
            file=file,
            prefix="products"
        )

        attachment = await AttachCrud.create_attachment(
            db=db,
            file_url=file_path_str,
            product_id=product_id
        )
        return attachment

    async def upload_category_icon(self, db: AsyncSession, file: UploadFile, category_id: int) -> Attachment:
        current_icon = await AttachCrud.get_by_category_id(db, category_id)
        current_file_url = current_icon.file_url if current_icon else None

        file_path_str = await save_file(
            file=file,
            current_file_url=current_file_url,
            prefix="categories"
        )

        if current_icon:
            # Если иконка уже была, обновляем только file_url
            current_icon.file_url = file_path_str
            await db.commit()
            await db.refresh(current_icon)
            return current_icon
        else:
            # Если иконки не было, создаем новую запись в БД
            attachment = await AttachCrud.create_attachment(
                db=db,
                file_url=file_path_str,
                category_id=category_id
            )
            return attachment

    async def delete_attachment(self, db: AsyncSession, attachment_id: int) -> None:
        attachment = await AttachCrud.get_by_id(db, attachment_id)

        if not attachment:
            raise ValueError(f"Attachment with id {attachment_id} not found")

        # 1. Удаление файла с диска
        await delete_file(attachment.file_url)

        # 2. Удаление записи из БД
        await AttachCrud.delete(db, attachment)


AttachmentService = AttachmentService()