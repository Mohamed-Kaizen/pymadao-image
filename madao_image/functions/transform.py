"""An image transform service."""
import base64
from enum import Enum
from io import BytesIO

from fastapi import APIRouter, File, Form, UploadFile
from PIL import Image
from pydantic import BaseModel

router = APIRouter()


class ImageResize(BaseModel):
    """Image resize model."""

    prefix: str = Form(None)

    width: int = Form(None)

    height: int = Form(None)

    @classmethod
    def __get_validators__(cls: "ImageResize") -> None:
        """Get validators."""
        yield cls.validate_with_json

    @classmethod
    def validate_with_json(cls: "ImageResize", value: str | int) -> dict:
        """Validate with json."""
        if value:
            return (
                cls.parse_raw(value) if isinstance(value, str) else cls.validate(value)
            )


class Format(str, Enum):
    """Format enum."""

    JPEG = "JPEG"

    PNG = "PNG"

    WEBP = "WEBP"


class ImageTransform(BaseModel):
    """Image transform model."""

    name: str

    base64: str


@router.post("/", response_model=list[ImageTransform])
async def transform(
    quality: int = Form(100),
    progressive: bool = Form(False),
    optimize: bool = Form(False),
    target_format: Format = Form(None),
    resize: list[ImageResize] | None = Form([]),
    image: UploadFile = File(...),
) -> list[ImageTransform]:
    """Transform the image."""
    file_bytes = await image.read()

    _image = Image.open(BytesIO(file_bytes))

    images: list[ImageTransform] = []

    _format = target_format.value if target_format else _image.format

    if all(resize):
        for item in resize:
            buffer = BytesIO()

            new_image = _image.resize((item.width, item.height))

            new_image.save(buffer, format=_format, quality=quality)

            images.append(
                ImageTransform(
                    name=item.prefix,
                    base64=base64.b64encode(buffer.getvalue()).decode("utf-8"),
                )
            )
    else:
        buffer = BytesIO()

        _image.save(
            buffer,
            format=_format,
            quality=quality,
            progressive=progressive,
            optimize=optimize,
        )

        images.append(
            ImageTransform(
                name="original",
                base64=base64.b64encode(buffer.getvalue()).decode("utf-8"),
            )
        )

    return images
