"""Main entry point for Todo App backend."""
from fastapi import FastAPI
from core.config import settings
from api.v1.tasks import router as tasks_router
from api.v1.auth import router as auth_router
from core.logging import logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from better_auth_integration import integrate_better_auth


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0",
        openapi_url="/api/v1/openapi.json" if settings.debug else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Next.js frontend
            "http://localhost:3001",  # Alternative Next.js port
            "http://127.0.0.1:3000",  # Alternative localhost format
            "http://127.0.0.1:3001",  # Alternative localhost format
            "http://localhost:8000",  # Self-origin for API testing
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose authorization header for JWT
        expose_headers=["Authorization"]
    )

    # Integrate Better Auth - this creates the compatible endpoints
    integrate_better_auth(app)

    # Include other API routers (auth, tasks, etc.)
    app.include_router(auth_router, prefix="/api/v1")  # Include the original auth endpoints
    app.include_router(tasks_router, prefix="/api/v1")

    @app.get("/")
    def read_root():
        """Root endpoint for health check."""
        return {"message": "Todo App Backend API", "version": "1.0.0"}

    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": "1.0.0"}

    return app


app = create_app()


if __name__ == "__main__":
    logger.info(f"Starting {settings.app_name} on 0.0.0.0:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )