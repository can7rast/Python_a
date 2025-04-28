from .musical_instrument import MusicalInstrument
from utils import NotificationMixin
from typing import Optional, Dict
from uuid import UUID
import logging


class Guitar(MusicalInstrument, NotificationMixin):
    """Класс для представления гитары, наследуется от MusicalInstrument."""

    def __init__(self, name: str, condition: str, daily_rate: float, number_of_strings: int):
        """Инициализирует объект гитары.

        Args:
            name: Название гитары.
            condition: Состояние гитары ('new', 'used', 'refurbished').
            daily_rate: Стоимость аренды за день.
            number_of_strings: Количество струн (от 4 до 12).

        Raises:
            ValueError: Если количество струн недопустимо.
            InvalidInstrumentError: Если параметры недопустимы.
        """
        super().__init__(name, condition, daily_rate)
        self._logger = logging.getLogger(self.__class__.__name__)
        if number_of_strings < 4 or number_of_strings > 12:
            raise ValueError("Количество струн должно быть от 4 до 12")
        self._number_of_strings: int = number_of_strings
        self.is_available = True  # Добавлено для совместимости с Rentable
        self._logger.info(f"Создана гитара: {name}")

    @property
    def number_of_strings(self) -> int:
        return self._number_of_strings

    @number_of_strings.setter
    def number_of_strings(self, value: int) -> None:
        if value < 4 or value > 12:
            raise ValueError("Количество струн должно быть от 4 до 12")
        self._number_of_strings = value
        self._logger.info(f"Изменено количество струн на: {value}")

    def rent_instrument(self) -> None:
        if not self.is_available:
            raise ValueError(f"Гитара {self.name} уже арендована")
        self.is_available = False
        self._logger.info(f"Гитара {self.name} арендована")

    def calculate_rental_cost(self, days: int) -> float:
        base_cost = self.daily_rate * days
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self._logger.info(f"Рассчитана стоимость аренды гитары {self.name} на {days} дней: {base_cost}")
        return base_cost

    def generate_report(self) -> str:
        return f"Отчет: Гитара {self.name}, Состояние: {self.condition}, Струн: {self._number_of_strings}"

    def to_dict(self) -> Dict:
        return {
            'type': 'guitar',
            'instrument_id': str(self.instrument_id),
            'name': self.name,
            'condition': self.condition,
            'daily_rate': self.daily_rate,
            'is_available': self.is_available,
            'number_of_strings': self.number_of_strings
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Guitar':
        return cls(
            name=data['name'],
            condition=data['condition'],
            daily_rate=data['daily_rate'],
            number_of_strings=data['number_of_strings']
        )

    def __str__(self) -> str:
        return f"Гитара: {self.name}, Состояние: {self.condition}, Струн: {self._number_of_strings}, Доступна: {self.is_available}"

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)