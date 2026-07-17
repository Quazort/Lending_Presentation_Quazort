import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from backend.app.core.database import db
from backend.app.core.log import get_logger
from backend.app.endpoints.general import general_router

logger = get_logger(__file__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI is ready to work")
    await db.init_db()
    yield
    await db.close()
    logger.info("FastAPI has finished its work")


main_app = FastAPI(title="Quazort_Lending", lifespan=lifespan)
main_app.mount("/static", StaticFiles(directory="static"), name="static")

main_app.include_router(general_router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Method: {request.method} | Path: {request.url.path} | "
        f"Status: {response.status_code} | Time: {process_time:.2f}ms | "
        f"IP: {request.client.host}"
    )

    return response


@main_app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Global error: {request.method} {request.url.path} | Error: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error"
        }
    )


@main_app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


@main_app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Global error: {request.method} {request.url.path} | Error: {str(exc)}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error"
        }
    )
