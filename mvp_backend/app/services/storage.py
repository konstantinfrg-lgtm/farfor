import os
import uuid
from pathlib import Path

import boto3
from fastapi import UploadFile

from app.core.config import settings

MEDIA_DIR = Path('media')
MEDIA_DIR.mkdir(exist_ok=True)


def upload_photo(file: UploadFile) -> str:
    ext = Path(file.filename or 'photo.jpg').suffix or '.jpg'
    key = f'items/{uuid.uuid4()}{ext}'

    if settings.s3_endpoint_url and settings.s3_access_key_id and settings.s3_secret_access_key:
        s3 = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint_url,
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
        )
        s3.upload_fileobj(file.file, settings.s3_bucket, key, ExtraArgs={'ContentType': file.content_type or 'image/jpeg'})
        base = settings.s3_endpoint_url.rstrip('/')
        return f'{base}/{settings.s3_bucket}/{key}'

    target = MEDIA_DIR / os.path.basename(key)
    with target.open('wb') as out:
        out.write(file.file.read())
    return f"{settings.media_base_url.rstrip('/')}/{target.name}"
