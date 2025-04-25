from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, Type
from uuid import UUID, uuid4

class InstrumentMeta(ABCMeta):
    _registry = {}  # Реестр подклассов

    def __new__(mcs, name, bases, attrs):
        new_cls = super().__new__(mcs, name, bases, attrs)
        if name != 'MusicalInstrument':  # Не регистрируем базовый класс
            mcs._registry[name.lower()] = new_cls
        return new_cls

    @classmethod
    def get_class(mcs, instrument_type: str) -> Optional[Type['MusicalInstrument']]:
        return mcs._registry.get(instrument_type.lower())

    @classmethod
    def create_instrument(mcs, instrument_type: str, *args, **kwargs) -> 'MusicalInstrument':
        """Создаёт экземпляр инструмента по имени типа."""
        cls = mcs.get_class(instrument_type)
        if not cls:
            raise ValueError(f"Инструмент типа '{instrument_type}' не зарегистрирован")
        return cls(*args, **kwargs)

    @classmethod
    def get_registered_classes(mcs) -> dict:
        """Возвращает реестр зарегистрированных классов."""
        return mcs._registry


class MusicalInstrument(ABC, metaclass=InstrumentMeta):

    def __init__(self, name: str, condition: str, daily_rate: float):
        self._instrument_id: UUID = uuid4()
        self._name: str = name
        self._condition: str = condition
        self._daily_rate: float = daily_rate
        self._is_available: bool = True

    # Геттеры
    @property
    def instrument_id(self) -> UUID:
        return self._instrument_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def daily_rate(self) -> float:
        return self._daily_rate

    @property
    def is_available(self) -> bool:
        return self._is_available

    # Сеттеры
    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Название инструмента не может быть пустым")
        self._name = value

    @condition.setter
    def condition(self, value: str) -> None:
        valid_conditions = ['new', 'used', 'refurbished']
        if value.lower() not in valid_conditions:
            raise ValueError(f"Состояние должно быть одним из: {valid_conditions}")
        self._condition = value.lower()

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        if value < 0:
            raise ValueError("Стоимость аренды не может быть отрицательной")
        self._daily_rate = value

    @is_available.setter
    def is_available(self, value: bool) -> None:
        self._is_available = value

    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        pass

    def __str__(self) -> str:
        return f"Инструмент: {self._name}, Состояние: {self._condition}, Доступен: {self._is_available}"

    def __lt__(self, other: 'MusicalInstrument') -> bool:
        if not isinstance(other, MusicalInstrument):
            return NotImplemented
        return self._daily_rate < other._daily_rate

    def __gt__(self, other: 'MusicalInstrument') -> bool:
        if not isinstance(other, MusicalInstrument):
            return NotImplemented
        return self._daily_rate > other._daily_rate