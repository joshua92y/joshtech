# apps/backend_admin/config/__init__.py
import asyncio
import threading
import logging

logger = logging.getLogger(__name__)


def start_ping():
    try:
        from ..utils.ping_flyio import ping_flyio

        logger.info("Starting FastAPI ping service...")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(ping_flyio())
    except Exception as e:
        logger.error(f"Error in ping service: {e}")


def run_background_ping():
    thread = threading.Thread(target=start_ping, daemon=True)
    thread.start()
    logger.info("Background ping thread started")


run_background_ping()
