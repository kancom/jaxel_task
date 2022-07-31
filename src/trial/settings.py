from pydantic import BaseSettings

from trial.application.foundation import Pair


class Settings(BaseSettings):
    pair: Pair = "USDTRUB"


class KafkaSettings(BaseSettings):
    topic: str = "jaxel"
    bootstrap_servers: str = "broker:9092"


class PollSettings(Settings, KafkaSettings):
    interval: int = 5


class PresentationSettings(Settings):
    db_dsn: str = "postgresql+asyncpg://jaxel:pass@db:5432/jaxel"


# db_dsn = "postgres://jaxel:pass@127.0.0.1:5001/jaxel"
# tortoise_orm = {
#     "connections": {"default": db_dsn},
#     "apps": {
#         "models": {
#             "models": ["src.trial.infrastructure.repository.tort_model"],
#             "default_connection": "default",
#         },
#     },
# }
