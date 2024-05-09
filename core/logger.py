from loguru import logger

from core.config import settings


logger.add(settings.LOG_FILE, level=settings.LOG_LEVEL)
