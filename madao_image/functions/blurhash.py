"""An blurhash service."""
import base64
from enum import Enum
from io import BytesIO

import blurhash as _blurhash
import numpy
from fastapi import APIRouter, File, Form, UploadFile
from PIL import Image
from pydantic import BaseModel

router = APIRouter()


class Format(str, Enum):
    """Format enum."""

    JPEG = "JPEG"

    PNG = "PNG"

    WEBP = "WEBP"


class ImageBlurhashHash(BaseModel):
    """Image blurhash hash model."""

    result: str

    height: float

    width: float


class ImageBlurhash(BaseModel):
    """Image transform model."""

    hash: ImageBlurhashHash

    image: str


@router.post("/", response_model=ImageBlurhash)
async def blurhash(
    components_x: int = Form(4),
    components_y: int = Form(4),
    target_format: Format = Form(None),
    image: UploadFile = File(...),
) -> ImageBlurhash:
    """Transform the image."""
    file_bytes = await image.read()

    _image = Image.open(BytesIO(file_bytes))

    height, width = _image.size

    _format = target_format.value if target_format else _image.format

    image_hash = _blurhash.encode(numpy.array(_image), components_x, components_y)

    blur_image = Image.fromarray(
        numpy.array(_blurhash.decode(image_hash, width, height)).astype("uint8")
    )

    buffer = BytesIO()

    blur_image.save(buffer, format=_format)

    return ImageBlurhash(
        **{
            "hash": {
                "result": image_hash,
                "width": width,
                "height": height,
            },
            "image": base64.b64encode(buffer.getvalue()).decode("utf-8"),
        }
    )
