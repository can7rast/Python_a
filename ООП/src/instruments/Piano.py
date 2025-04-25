from .musical_instrument import MusicalInstrument
from utils import LoggingMixin, NotificationMixin
from typing import Optional
from uuid import UUID

class Piano(MusicalInstrument, LoggingMixin, NotificationMixin):
    """Класс для представления пианино."""

    def __init__(self, name: str, condition: str, daily_rate: float, key_count: int):
        """Инициализация пианино."""
        super().__init__(name, condition, daily_rate)
        self._key_count: int = key_count
        self.log_action(f"Создано пианино {name}")

    @property
    def key_count(self) -> int:
        """Возвращает количество клавиш."""
        return self._key_count

    @key_count.setter
    def key_count(self, value: int) -> None:
        """Устанавливает количество клавиш."""
        if value < 61 or value > 88:
            raise ValueError("Количество клавиш должно быть от 61 до 88")
        self._key_count = value
        self.log_action(f"Изменено количество клавиш на {value}")

    def calculate_rental_cost(self, days: int) -> float:
        """Рассчитывает стоимость аренды пианино."""
        base_cost = self.daily_rate * days
        if self._key_count > 76:
            base_cost *= 1.2  # Премиум-тариф 20% для пианино с более чем 76 клавишами
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self.log_action(f"Рассчитана стоимость аренды пианино {self.name} на {days} дней: {base_cost}")
        return base_cost

    def __str__(self) -> str:
        """Возвращает строковое представление пианино."""
        return f"Пианино: {self.name}, Состояние: {self.condition}, Клавиш: {self._key_count}, Доступно: {self.is_available}"