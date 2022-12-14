"""The app for madao image."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .functions import blurhash, transform
from .settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(transform.router, prefix="/transform", tags=["transform"])
app.include_router(blurhash.router, prefix="/blurhash", tags=["blurhash"])
