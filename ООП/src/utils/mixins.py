class NotificationMixin:
    """Миксин для отправки уведомлений клиентам."""

    def notify(self, message: str) -> None:
        """Отправляет уведомление с указанным сообщением.

        Args:
            message: Текст уведомления.
        """
        print(f"Уведомление: {message}")