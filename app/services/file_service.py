from __future__ import annotations

import os
import secrets
from pathlib import Path

from PIL import Image
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_image(file_storage: FileStorage) -> str:
    if not file_storage.filename:
        raise ValueError("Пустое имя файла")

    filename = secure_filename(file_storage.filename)
    if not allowed_file(filename):
        raise ValueError("Недопустимый тип файла")

    ext = filename.rsplit(".", 1)[1].lower()
    generated = f"{secrets.token_hex(16)}.{ext}"
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    target = upload_folder / generated
    file_storage.save(target)

    with Image.open(target) as img:
        img.verify()

    return generated


def remove_image(filename: str) -> None:
    path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    if path.exists():
        os.remove(path)
