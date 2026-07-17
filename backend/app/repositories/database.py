from sqlalchemy import select, func

from backend.app.models.leads import LeadModel, CommentStatus
from backend.app.schemas.metrics import MetricsSchema



async def create_lead(session, feedback, ai_response: str = None, ai_tone: str = None,
                      status: CommentStatus = CommentStatus.SUCCESS) -> None:

    if status != CommentStatus.FAILED and ai_response is None:
        status = CommentStatus.AI_ERROR
    db_tone = ai_tone.value if hasattr(ai_tone, "value") else ai_tone
    new_lead = LeadModel(
        user_name=feedback.name,
        user_phone=feedback.phone,
        user_email=feedback.email,
        comment=feedback.comment,
        ai_response=ai_response,
        comment_tone=db_tone,
        status=status.value
    )
    session.add(new_lead)

async def get_metrics_from_db(session) -> MetricsSchema:
    query_status = select(LeadModel.status, func.count(LeadModel.id)).group_by(LeadModel.status)
    result_status = await session.execute(query_status)
    status_rows = result_status.all()

    query_tone = select(LeadModel.comment_tone, func.count(LeadModel.id)).group_by(LeadModel.comment_tone)
    result_tone = await session.execute(query_tone)
    tone_rows = result_tone.all()

    tone_data = {"NEGATIVE": 0, "POSITIVE": 0, "NEUTRAL": 0}
    status_data = {"SUCCESS": 0, "FAILED": 0, "AI_ERROR": 0, "TOTAL": 0}


    for db_status, count in status_rows:
        if db_status:
            status_key = db_status.value
            if status_key in status_data:
                status_data[status_key] = count
                status_data["TOTAL"] += count

    for db_tone, count in tone_rows:
        if db_tone:
            if db_tone in tone_data:
                tone_data[db_tone] = count

    return MetricsSchema(request_statuses=status_data, tone_of_appeals=tone_data)