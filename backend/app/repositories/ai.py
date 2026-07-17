from backend.app.core.config import settings
from openai import AsyncOpenAI, AuthenticationError, APITimeoutError

from backend.app.core.log import get_logger
from backend.app.schemas.feedback import AIResponseSchema

logger = get_logger(__name__)


class AI:
    def __init__(self, role):
        self.role = role
        self.client = AsyncOpenAI(
            api_key=settings.AI_KEY,
            base_url=settings.BASE_API_AI,
            timeout=15)

    async def __call__(self, text: str) -> AIResponseSchema | None:
        ai_response = None
        for _ in range(2):
            try:
                ai_response = await self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": self.role},
                        {"role": "user", "content": text},
                    ],
                    temperature=0.7,
                    response_format={'type': 'json_object'},
                    stream=False)
                raw_content = ai_response.choices[0].message.content
                parsed_data = AIResponseSchema.model_validate_json(raw_content)
                return parsed_data
            except AuthenticationError as e:
                logger.error(f"Key problem:{e}")
                break
            except APITimeoutError:
                logger.error("Request timed out")
            except Exception as e:
                logger.error(f"AI malfunction: {e}")

        return ai_response
