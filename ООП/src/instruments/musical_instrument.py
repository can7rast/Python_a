from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, Type, Dict
from uuid import UUID, uuid4
from utils import InvalidInstrumentError
import logging


class InstrumentMeta(ABCMeta):
    """Метакласс для регистрации подклассов музыкальных инструментов."""

    _registry: Dict[str, type] = {}  # Реестр подклассов

    def __new__(mcs, name, bases, attrs):
        """Создаёт новый класс и регистрирует его, если это не базовый класс.

        Args:
            name: Имя класса.
            bases: Кортеж базовых классов.
            attrs: Словарь атрибутов класса.

        Returns:
            Новый класс.
        """
        new_cls = super().__new__(mcs, name, bases, attrs)
        if name != 'MusicalInstrument':  # Не регистрируем базовый класс
            mcs._registry[name.lower()] = new_cls
        return new_cls

    @classmethod
    def get_class(mcs, instrument_type: str) -> Optional[Type['MusicalInstrument']]:
        """Возвращает класс инструмента по его типу.

        Args:
            instrument_type: Тип инструмента (например, 'guitar').

        Returns:
            Класс инструмента или None, если тип не найден.
        """
        return mcs._registry.get(instrument_type.lower())

    @classmethod
    def create_instrument(mcs, instrument_type: str, *args, **kwargs) -> 'MusicalInstrument':
        """Создаёт экземпляр инструмента по имени типа.

        Args:
            instrument_type: Тип инструмента.
            *args: Позиционные аргументы для инициализации.
            **kwargs: Именованные аргументы для инициализации.

        Returns:
            Экземпляр инструмента.

        Raises:
            ValueError: Если тип инструмента не зарегистрирован.
        """
        cls = mcs.get_class(instrument_type)
        if not cls:
            raise ValueError(f"Инструмент типа '{instrument_type}' не зарегистрирован")
        return cls(*args, **kwargs)

    @classmethod
    def get_registered_classes(mcs) -> Dict[str, type]:
        return mcs._registry


class MusicalInstrument(ABC, metaclass=InstrumentMeta):
    """Абстрактный базовый класс для музыкальных инструментов."""

    # Порядок состояний для сравнения
    _CONDITION_ORDER = {'new': 2, 'refurbished': 1, 'used': 0}

    def __init__(self, name: str, condition: str, daily_rate: float):
        """Инициализирует музыкальный инструмент.

        Args:
            name: Название инструмента.
            condition: Состояние инструмента ('new', 'used', 'refurbished').
            daily_rate: Стоимость аренды за день.

        Raises:
            InvalidInstrumentError: Если параметры недопустимы.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._instrument_id: UUID = uuid4()
        if not name.strip():
            raise InvalidInstrumentError("Название инструмента не может быть пустым")
        if condition.lower() not in ["new", "used", "refurbished"]:
            raise InvalidInstrumentError("Состояние инструмента должно быть 'new', 'used' или 'refurbished'")
        if daily_rate <= 0:
            raise InvalidInstrumentError("Стоимость аренды должна быть положительной")
        self._name: str = name
        self._condition: str = condition.lower()
        self._daily_rate: float = daily_rate
        self._is_available: bool = True
        self._logger.info(f"Создан инструмент: {name}")

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

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise InvalidInstrumentError("Название инструмента не может быть пустым")
        self._name = value
        self._logger.info(f"Изменено название инструмента на: {value}")

    @condition.setter
    def condition(self, value: str) -> None:
        valid_conditions = ['new', 'used', 'refurbished']
        if value.lower() not in valid_conditions:
            raise InvalidInstrumentError(f"Состояние должно быть одним из: {valid_conditions}")
        self._condition = value.lower()
        self._logger.info(f"Изменено состояние инструмента на: {value}")

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        if value <= 0:
            raise InvalidInstrumentError("Стоимость аренды должна быть положительной")
        self._daily_rate = value
        self._logger.info(f"Изменена стоимость аренды на: {value}")

    @is_available.setter
    def is_available(self, value: bool) -> None:
        self._is_available = value
        self._logger.info(f"Изменена доступность инструмента на: {value}")

    def rent_instrument(self) -> None:
        if not self._is_available:
            raise ValueError(f"Инструмент {self._name} уже арендован")
        self._is_available = False
        self._logger.info(f"Инструмент {self._name} арендован")

    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @classmethod
    def from_dict(cls, data: Dict) -> 'MusicalInstrument':
        """Создаёт объект из словаря.

        Args:
            data: Словарь с данными об инструменте.

        Returns:
            Экземпляр инструмента.

        Raises:
            ValueError: Если тип инструмента неизвестен.
        """
        instrument_type = data.get('type', '').lower()
        cls = cls.get_class(instrument_type)
        if not cls:
            raise ValueError(f"Неизвестный тип инструмента: {instrument_type}")
        return cls.from_dict(data)

    def __str__(self) -> str:
        return f"Инструмент: {self._name}, Состояние: {self._condition}, Доступен: {self._is_available}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MusicalInstrument):
            return NotImplemented
        return (self._daily_rate == other._daily_rate and
                self._CONDITION_ORDER[self._condition] == self._CONDITION_ORDER[other._condition])

    def __lt__(self, other: 'MusicalInstrument') -> bool:
        if not isinstance(other, MusicalInstrument):
            return NotImplemented
        if self._daily_rate != other._daily_rate:
            return self._daily_rate < other._daily_rate
        return self._CONDITION_ORDER[self._condition] < self._CONDITION_ORDER[other._condition]

    def __gt__(self, other: 'MusicalInstrument') -> bool:
        if not isinstance(other, MusicalInstrument):
            return NotImplemented
        if self._daily_rate != other._daily_rate:
            return self._daily_rate > other._daily_rate
        return self._CONDITION_ORDER[self._condition] > self._CONDITION_ORDER[other._condition]