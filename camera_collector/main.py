import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from camera_collector.core.config import settings
from camera_collector.db.database import connect_to_mongodb, close_mongodb_connection
from camera_collector.api.routers import auth, cameras, stats


app = FastAPI(
    title="Vintage Camera Collection API",
    description="API for managing a collection of vintage cameras",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Add event handlers
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongodb()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()


# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(cameras.router, prefix=settings.API_PREFIX)
app.include_router(stats.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Vintage Camera Collection API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
    }


if __name__ == "__main__":
    uvicorn.run("camera_collector.main:app", host="0.0.0.0", port=8000, reload=True)