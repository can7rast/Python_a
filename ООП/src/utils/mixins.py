import logging
import os
from datetime import datetime

class LoggingMixin:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            os.makedirs('logs', exist_ok=True)
            file_handler = logging.FileHandler(
                f"logs/rental_service_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
            ))
            self.logger.addHandler(file_handler)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
            ))
            self.logger.addHandler(console_handler)

    def log(self, message: str) -> None:
        self.logger.info(message)

class NotificationMixin:
    def notify(self, message: str) -> None:
        print(f"[УВЕДОМЛЕНИЕ] {message}")