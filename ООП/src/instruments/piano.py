from .musical_instrument import MusicalInstrument
from utils import NotificationMixin
from typing import Optional, Dict
from uuid import UUID
import logging


class Piano(MusicalInstrument, NotificationMixin):
    """Класс для представления пианино, наследуется от MusicalInstrument."""

    def __init__(self, name: str, condition: str, daily_rate: float, key_count: int):
        """Инициализирует объект пианино.

        Args:
            name: Название пианино.
            condition: Состояние пианино ('new', 'used', 'refurbished').
            daily_rate: Стоимость аренды за день.
            key_count: Количество клавиш (от 61 до 88).

        Raises:
            ValueError: Если количество клавиш недопустимо.
            InvalidInstrumentError: Если параметры недопустимы.
        """
        super().__init__(name, condition, daily_rate)
        self._logger = logging.getLogger(self.__class__.__name__)
        if key_count < 61 or key_count > 88:
            raise ValueError("Количество клавиш должно быть от 61 до 88")
        self._key_count: int = key_count
        self.is_available = True  # Добавлено для совместимости с Rentable
        self._logger.info(f"Создано пианино: {name}")

    @property
    def key_count(self) -> int:
        return self._key_count

    @key_count.setter
    def key_count(self, value: int) -> None:
        if value < 61 or value > 88:
            raise ValueError("Количество клавиш должно быть от 61 до 88")
        self._key_count = value
        self._logger.info(f"Изменено количество клавиш на: {value}")

    def rent_instrument(self) -> None:
        if not self.is_available:
            raise ValueError(f"Пианино {self.name} уже арендовано")
        self.is_available = False
        self._logger.info(f"Пианино {self.name} арендовано")

    def calculate_rental_cost(self, days: int) -> float:
        base_cost = self.daily_rate * days
        if self._key_count > 76:
            base_cost *= 1.2  # Премиум-тариф 20% для пианино с более чем 76 клавишами
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self._logger.info(f"Рассчитана стоимость аренды пианино {self.name} на {days} дней: {base_cost}")
        return base_cost

    def generate_report(self) -> str:
        return f"Отчет: Пианино {self.name}, Состояние: {self.condition}, Клавиш: {self._key_count}"

    def to_dict(self) -> Dict:
        return {
            'type': 'piano',
            'instrument_id': str(self.instrument_id),
            'name': self.name,
            'condition': self.condition,
            'daily_rate': self.daily_rate,
            'is_available': self.is_available,
            'key_count': self.key_count
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Piano':
        return cls(
            name=data['name'],
            condition=data['condition'],
            daily_rate=data['daily_rate'],
            key_count=data['key_count']
        )

    def __str__(self) -> str:
        return f"Пианино: {self.name}, Состояние: {self.condition}, Клавиш: {self._key_count}, Доступно: {self.is_available}"

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)