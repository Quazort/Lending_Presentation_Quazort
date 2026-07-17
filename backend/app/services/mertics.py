from backend.app.core.database import db
from backend.app.core.log import get_logger
from backend.app.repositories.database import get_metrics_from_db
from backend.app.schemas.metrics import MetricsSchema

logger = get_logger(__file__)


async def get_metrics() -> MetricsSchema:
    async with db.session_scope() as session:
        result = await get_metrics_from_db(session=session)
        return result
