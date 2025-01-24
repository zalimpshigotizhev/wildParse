import logging
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from v1.logic.scheduler.db import upd_all_auto_up_products_to_db

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом планировщика приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.
    """
    try:
        # Настройка и запуск планировщика
        scheduler.add_job(
            upd_all_auto_up_products_to_db,
            trigger=IntervalTrigger(minutes=30),
            id='currency_update_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started")
        yield
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        # Завершение работы планировщика
        scheduler.shutdown()
