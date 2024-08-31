from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version=settings.API_VERSION,
    root_path=settings.ROOT_PATH,
    openapi_url=f"{settings.ROOT_PATH}/openapi.json",
    docs_url=f"{settings.ROOT_PATH}/docs",
    redoc_url=f"{settings.ROOT_PATH}/redoc",
    swagger_ui_oauth2_redirect_url=f"{settings.ROOT_PATH}/docs/oauth2-redirect",
    servers=[{"url": settings.ROOT_PATH}],
)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}
