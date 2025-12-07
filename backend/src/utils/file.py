import os
import string
import uuid
import shutil
from pathlib import Path
import random
from typing import Optional
from fastapi import UploadFile

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]
UPLOAD_DIR = Path("../../static")

async def save_file(file: UploadFile, current_file_url: Optional[str] = None, prefix: str = "") -> str:
    # Проверка типа файла
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Неподдерживаемый тип файла. Разрешены только: {', '.join(ALLOWED_IMAGE_TYPES)}")

    # Удаление старого файла, если он существует
    if current_file_url:
        old_file_path = UPLOAD_DIR / prefix / os.path.basename(current_file_url)
        if old_file_path.exists():
            old_file_path.unlink()

    # Генерация уникального имени файла
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{random.choices(string.digits, k=6)}_{uuid.uuid4()}.{file_extension}"

    # Путь для сохранения файла с учетом префикса
    target_dir = UPLOAD_DIR / prefix
    target_dir.mkdir(parents=True, exist_ok=True)  # Создает директорию, если её нет

    file_path = target_dir / unique_filename

    # Сохранение файла на диск
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)

async def delete_file(file_url: Optional[str]) -> None:
    if not file_url:
        return

    file_path = Path(file_url)
    if not file_path.is_absolute():
        file_path = UPLOAD_DIR / file_path

    if file_path.exists():
        file_path.unlink()