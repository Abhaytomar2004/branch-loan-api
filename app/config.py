import os
import logging
from pythonjsonlogger import jsonlogger

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL = os.getenv("DATABASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @staticmethod
    def setup_logging():
        logger = logging.getLogger()
        
        if Config.ENVIRONMENT == "production":
            # JSON logging for production
            log_handler = logging.StreamHandler()
            formatter = jsonlogger.JsonFormatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s"
            )
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
        else:
            # Simple logging for development
            logging.basicConfig(
                level=Config.LOG_LEVEL,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
