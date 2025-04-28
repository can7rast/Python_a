from .musical_instrument import MusicalInstrument
from utils import NotificationMixin
from typing import Optional, Dict
from uuid import UUID
import logging


class Violin(MusicalInstrument, NotificationMixin):
    """Класс для представления скрипки, наследуется от MusicalInstrument."""

    def __init__(self, name: str, condition: str, daily_rate: float, bow_included: bool):
        """Инициализирует объект скрипки.

        Args:
            name: Название скрипки.
            condition: Состояние скрипки ('new', 'used', 'refurbished').
            daily_rate: Стоимость аренды за день.
            bow_included: Наличие смычка в комплекте.

        Raises:
            InvalidInstrumentError: Если параметры недопустимы.
        """
        super().__init__(name, condition, daily_rate)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._bow_included: bool = bow_included
        self.is_available = True  # Добавлено для совместимости с Rentable
        self._logger.info(f"Создана скрипка: {name}")

    @property
    def bow_included(self) -> bool:
        return self._bow_included

    @bow_included.setter
    def bow_included(self, value: bool) -> None:
        self._bow_included = value
        self._logger.info(f"Изменено наличие смычка: {value}")

    def rent_instrument(self) -> None:
        if not self.is_available:
            raise ValueError(f"Скрипка {self.name} уже арендована")
        self.is_available = False
        self._logger.info(f"Скрипка {self.name} арендована")

    def calculate_rental_cost(self, days: int) -> float:
        base_cost = self.daily_rate * days
        if self._bow_included:
            base_cost += 10 * days  # Дополнительная плата 10 за день за смычок
        if days > 7:
            base_cost *= 0.8  # Скидка 20% за аренду более 7 дней
        self._logger.info(f"Рассчитана стоимость аренды скрипки {self.name} на {days} дней: {base_cost}")
        return base_cost

    def generate_report(self) -> str:
        return f"Отчет: Скрипка {self.name}, Состояние: {self.condition}, Смычок: {'включен' if self._bow_included else 'не включен'}"

    def to_dict(self) -> Dict:
        return {
            'type': 'violin',
            'instrument_id': str(self.instrument_id),
            'name': self.name,
            'condition': self.condition,
            'daily_rate': self.daily_rate,
            'is_available': self.is_available,
            'bow_included': self.bow_included
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Violin':
        return cls(
            name=data['name'],
            condition=data['condition'],
            daily_rate=data['daily_rate'],
            bow_included=data['bow_included']
        )

    def __str__(self) -> str:
        return f"Скрипка: {self.name}, Состояние: {self.condition}, Смычок: {'включен' if self._bow_included else 'не включен'}, Доступна: {self.is_available}"

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)