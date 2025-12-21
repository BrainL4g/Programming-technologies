from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.service.attachment import AttachmentService
from src.schema.attachment import AttachmentResponse
from src.exceptions import FileNotFound
from src.repository.attachment import AttachCrud
from typing import List

from src.service.product import ProductService

router = APIRouter(tags=["Attachments"])

@router.get("/uploads/{attachment_id}", status_code=status.HTTP_200_OK)
async def get_file(attachment_id: int,
                   db: AsyncSession = Depends(get_db_session)):
    file = await AttachCrud.get_by_id(db=db, attachment_id=attachment_id)
    if not file:
        raise FileNotFound()
    print(file.file_url)
    return FileResponse(file.file_url)

@router.post("/products/{product_id}/images", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_product_image(
        product_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser)
):
    product = await ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    try:
        return await AttachmentService.upload_product_image(db, file, product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/categories/{category_id}/icon", response_model=AttachmentResponse)
async def upload_category_icon(
        category_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser)
):
    # TODO: Проверить существование Category с category_id

    try:
        return await AttachmentService.upload_category_icon(db, file, category_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
        attachment_id: int,
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser)
):
    try:
        await AttachmentService.delete_attachment(db, attachment_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")