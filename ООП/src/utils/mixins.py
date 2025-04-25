import logging
from datetime import datetime

# Настройка логгера
logging.basicConfig(
    filename='logs/rental_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LoggingMixin:
    """Миксин для логирования действий."""

    def log_action(self, message: str) -> None:
        """Записывает действие в лог.

        Args:
            message: Сообщение для логирования.
        """
        logging.info(f"{self.__class__.__name__}: {message}")

class NotificationMixin:
    """Миксин для отправки уведомлений."""

    def send_notification(self, message: str, recipient: str) -> None:
        """Имитирует отправку уведомления.

        Args:
            message: Сообщение для отправки.
            recipient: Получатель (например, email).
        """
        print(f"[УВЕДОМЛЕНИЕ] {message} для {recipient}")