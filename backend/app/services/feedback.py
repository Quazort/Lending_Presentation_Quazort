from backend.app.core.config import settings
from backend.app.core.database import db
from backend.app.core.log import get_logger
from backend.app.models.leads import CommentStatus
from backend.app.repositories.ai import AI
from backend.app.repositories.database import create_lead
from backend.app.repositories.mail import Email

logger = get_logger(__file__)

agent = AI(settings.AI_SYSTEM_PROMPT)
mail = Email()



async def handle_feedback_background(feedback) -> None:
    logger.info(f"Started background processing for lead: {feedback.email}")

    ai_data = await agent(feedback.comment)

    ai_comment_tone = None
    ai_response = None

    if ai_data:
        ai_comment_tone = ai_data.comment_tone
        ai_response = ai_data.response

    user_body = (
        f"Здравствуйте, {feedback.name.capitalize()}!\n"
        f"Вы оставили свое сообщение на сайте Lending Quazort Test:\n"
        f"\"{feedback.comment}\"\n"
        f"Ваше сообщение принято в обработку, скоро с вами свяжутся, ожидайте."
    )
    admin_body = (
        f"Новая заявка на сайте!\n"
        f"Имя: {feedback.name}\n"
        f"Телефон: {feedback.phone}\n"
        f"Email: {feedback.email}\n"
        f"Комментарий:\n{feedback.comment}"
    )

    if ai_response:
        ai_suffix = f"\n\nПредварительный ответ нашего ИИ:\n{ai_response}"
        user_body += ai_suffix
        admin_body += ai_suffix

    user_sent = await mail(
        receiver_email=feedback.email,
        subject="Ваше обращение принято - Quazort",
        body=user_body
    )
    admin_sent = await mail(
        receiver_email=settings.ADMIN_EMAIL,
        subject="Новое обращение с Lending Quazort!",
        body=admin_body
    )

    if not user_sent or not admin_sent:
        db_status = CommentStatus.FAILED
        logger.error(f"Failed to deliver one or both emails for {feedback.email}.")
    elif ai_response is None:
        db_status = CommentStatus.AI_ERROR
        logger.error(f"Emails successfully sent without AI for {feedback.email}.")
    else:
        db_status = CommentStatus.SUCCESS
        logger.info(f"Successfully deliver both emails for {feedback.email}.")

    try:
        async with db.session_scope() as session:
            await create_lead(
                session=session,
                feedback=feedback,
                ai_response=ai_response,
                ai_tone=ai_comment_tone,
                status=db_status
            )
        logger.info(
            f"Feedback processing completed successfully for {feedback.email}. Status in DB: {db_status.value}")

    except Exception as e:
        logger.critical(f"Complete error when saving to DB for {feedback.email}: {e}")

    return None
