from .musical_instrument import MusicalInstrument
from utils import LoggingMixin, NotificationMixin
from typing import Optional
from uuid import UUID

class Guitar(MusicalInstrument, LoggingMixin, NotificationMixin):
    """Класс для представления гитары."""

    def __init__(self, name: str, condition: str, daily_rate: float, number_of_strings: int):
        """Инициализация гитары."""
        super().__init__(name, condition, daily_rate)
        self._number_of_strings: int = number_of_strings
        self.log_action(f"Создана гитара {name}")

    @property
    def number_of_strings(self) -> int:
        """Возвращает количество струн."""
        return self._number_of_strings

    @number_of_strings.setter
    def number_of_strings(self, value: int) -> None:
        """Устанавливает количество струн."""
        if value < 4 or value > 12:
            raise ValueError("Количество струн должно быть от 4 до 12")
        self._number_of_strings = value
        self.log_action(f"Изменено количество струн на {value}")

    def calculate_rental_cost(self, days: int) -> float:
        """Рассчитывает стоимость аренды гитары."""
        base_cost = self.daily_rate * days
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self.log_action(f"Рассчитана стоимость аренды гитары {self.name} на {days} дней: {base_cost}")
        return base_cost

    def __str__(self) -> str:
        """Возвращает строковое представление гитары."""
        return f"Гитара: {self.name}, Состояние: {self.condition}, Струн: {self._number_of_strings}, Доступна: {self.is_available}"