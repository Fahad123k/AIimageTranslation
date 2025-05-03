from fastapi import FastAPI
from config.settings import settings
from routers import home_router, text_translate_router, image_translate_router
from fastapi.staticfiles import StaticFiles

def create_app():
    app = FastAPI(
        title=settings.APP_TITLE or "My FastAPI App",
        version=settings.APP_VERSION or "1.0.0",
    )

    # Include routers
    app.include_router(home_router.router)
    app.include_router(text_translate_router.router)
    app.include_router(image_translate_router.router)

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app