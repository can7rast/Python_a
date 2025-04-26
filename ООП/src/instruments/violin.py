from .musical_instrument import MusicalInstrument
from utils import LoggingMixin, NotificationMixin
from typing import Optional
from uuid import UUID

class Violin(MusicalInstrument, LoggingMixin, NotificationMixin):
    """Класс для представления скрипки."""

    def __init__(self, name: str, condition: str, daily_rate: float, bow_included: bool):
        """Инициализация скрипки."""
        LoggingMixin.__init__(self)  # Явная инициализация LoggingMixin
        super().__init__(name, condition, daily_rate)
        self._bow_included: bool = bow_included
        self.is_available = True  # Добавлено для совместимости с Rentable
        self.log(f"Создана скрипка {name}")

    @property
    def bow_included(self) -> bool:
        """Возвращает наличие смычка."""
        return self._bow_included

    @bow_included.setter
    def bow_included(self, value: bool) -> None:
        """Устанавливает наличие смычка."""
        self._bow_included = value
        self.log(f"Изменено наличие смычка: {value}")

    def rent_instrument(self) -> None:
        """Арендует скрипку."""
        if not self.is_available:
            raise ValueError(f"Скрипка {self.name} уже арендована")
        self.is_available = False
        self.log(f"Скрипка {self.name} арендована")

    def calculate_rental_cost(self, days: int) -> float:
        """Рассчитывает стоимость аренды скрипки."""
        base_cost = self.daily_rate * days
        if self._bow_included:
            base_cost += 10 * days  # Дополнительная плата 10 за день за смычок
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self.log(f"Рассчитана стоимость аренды скрипки {self.name} на {days} дней: {base_cost}")
        return base_cost

    def generate_report(self) -> str:
        """Генерирует отчет для скрипки."""
        return f"Отчет: Скрипка {self.name}, Состояние: {self.condition}, Смычок: {'включен' if self._bow_included else 'не включен'}"

    def __str__(self) -> str:
        """Возвращает строковое представление скрипки."""
        return f"Скрипка: {self.name}, Состояние: {self.condition}, Смычок: {'включен' if self._bow_included else 'не включен'}, Доступна: {self.is_available}"