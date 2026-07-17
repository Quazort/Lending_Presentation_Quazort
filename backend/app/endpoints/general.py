from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status
from starlette.responses import FileResponse

from backend.app.schemas.feedback import FeedbackRequestSchema, FeedbackResponseSchema
from backend.app.services.feedback import handle_feedback_background
from backend.app.services.mertics import get_metrics
from backend.app.services.rate_limiter import check_contact_rate_limit

general_router = APIRouter()


@general_router.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@general_router.post("/api/contact",dependencies=[Depends(check_contact_rate_limit)], status_code=status.HTTP_201_CREATED)
async def contact(feedback: FeedbackRequestSchema,
                  background_tasks: BackgroundTasks):
    background_tasks.add_task(
        handle_feedback_background,
        feedback=feedback
    )
    return FeedbackResponseSchema()


@general_router.get("/api/health")
async def health():
    return {"status": "alive", "service": "quazort-backend"}


@general_router.get("/api/metrics")
async def metrics():
    result = await get_metrics()
    return result
