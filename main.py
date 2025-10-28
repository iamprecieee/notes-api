from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.database import close_database_connection, connect_to_database
from loguru import logger

from core.exceptions import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_database()
    logger.info("Connected to MongoDB")

    yield

    await close_database_connection()
    logger.info("Closed MongoDB connection")


app = FastAPI(
    title="Notes API",
    description="Multi-tenant notes API with role-based access control",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(AuthenticationError)
async def authentication_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc)},
    )


@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc)},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc)},
    )


@app.exception_handler(ConflictError)
async def conflict_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc)},
    )


from api import organization, user, auth, note

app.include_router(organization.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(note.router)


@app.get("/")
async def root():
    return {"message": "Notes API", "version": "1.0.0"}
