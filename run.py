from src.telegram import start_bot
import asyncio
from src.database.tables import create_db
from src.my_logger import logger


if __name__ == '__main__':
    create_db()
    logger.info("Bot started")
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by admin")