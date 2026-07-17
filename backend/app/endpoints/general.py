from fastapi import APIRouter

general_router = APIRouter()


@general_router.post("/api/contact")
async def contact():
    pass


@general_router.get("/api/health")
async def health():
    pass


@general_router.get("/api/metrics")
async def metrics():
    pass
