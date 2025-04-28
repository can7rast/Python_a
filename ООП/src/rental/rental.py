from uuid import UUID, uuid4
from datetime import datetime, date
from typing import List, Optional, Dict
from .customer import Customer
from .accessory import Accessory
from instruments.musical_instrument import MusicalInstrument
from .interfaces import Rentable, Reportable
from utils import NotificationMixin, check_permissions, RentalNotFoundError
import logging


class Rental(Rentable, Reportable, NotificationMixin):
    """Класс для управления арендой музыкальных инструментов."""

    _rentals: List['Rental'] = []  # Реестр всех аренд

    def __init__(
            self,
            customer: Customer,
            instrument: MusicalInstrument,
            start_date: date,
            end_date: date
    ):
        """Инициализирует объект аренды.

        Args:
            customer: Клиент, арендующий инструмент.
            instrument: Музыкальный инструмент.
            start_date: Дата начала аренды.
            end_date: Дата окончания аренды.

        Raises:
            ValueError: Если дата начала позже даты окончания.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        if start_date > end_date:
            raise ValueError("Дата начала аренды не может быть позже даты окончания")
        self._rental_id: UUID = uuid4()
        self._customer: Customer = customer
        self._instrument: MusicalInstrument = instrument
        self._start_date: date = start_date
        self._end_date: date = end_date
        self._accessories: List[Accessory] = []
        self._total_cost: float = 0.0
        self.calculate_total()
        self._rentals.append(self)  # Добавляем аренду в реестр
        self._logger.info(f"Создана аренда #{self._rental_id} для {customer.name}")
        self.notify(
            f"Ваш инструмент {instrument.name} готов к выдаче для {customer.email}"
        )

    @property
    def rental_id(self) -> UUID:
        """Возвращает уникальный идентификатор аренды.

        Returns:
            UUID аренды.
        """
        return self._rental_id

    @property
    def customer(self) -> Customer:
        """Возвращает клиента, арендующего инструмент.

        Returns:
            Объект клиента.
        """
        return self._customer

    @property
    def instrument(self) -> MusicalInstrument:
        """Возвращает арендованный инструмент.

        Returns:
            Объект инструмента.
        """
        return self._instrument

    @property
    def start_date(self) -> date:
        """Возвращает дату начала аренды.

        Returns:
            Дата начала аренды.
        """
        return self._start_date

    @property
    def end_date(self) -> date:
        """Возвращает дату окончания аренды.

        Returns:
            Дата окончания аренды.
        """
        return self._end_date

    @property
    def total_cost(self) -> float:
        """Возвращает общую стоимость аренды.

        Returns:
            Общая стоимость аренды.
        """
        return self._total_cost

    @property
    def accessories(self) -> List[Accessory]:
        """Возвращает список аксессуаров, включённых в аренду.

        Returns:
            Список аксессуаров.
        """
        return self._accessories

    @check_permissions("can_modify_rental")
    def add_accessory(self, accessory: Accessory) -> None:
        """Добавляет аксессуар к аренде.

        Args:
            accessory: Аксессуар для добавления.
        """
        self._accessories.append(accessory)
        self.calculate_total()
        self._logger.info(f"Добавлен аксессуар {accessory.name} к аренде #{self._rental_id}")

    @check_permissions("can_modify_rental")
    def remove_accessory(self, accessory_id: UUID) -> None:
        """Удаляет аксессуар из аренды.

        Args:
            accessory_id: Идентификатор аксессуара.

        Raises:
            ValueError: Если аксессуар не найден.
        """
        for accessory in self._accessories:
            if accessory.accessory_id == accessory_id:
                self._accessories.remove(accessory)
                self.calculate_total()
                self._logger.info(f"Удален аксессуар {accessory.name} из аренды #{self._rental_id}")
                return
        raise ValueError("Аксессуар не найден")

    def calculate_total(self) -> None:
        """Рассчитывает общую стоимость аренды, включая инструмент и аксессуары."""
        days = (self._end_date - self._start_date).days
        if days <= 0:
            self._total_cost = 0.0
            return
        instrument_cost = self._instrument.calculate_rental_cost(days)
        accessories_cost = sum(accessory.cost * days for accessory in self._accessories)
        self._total_cost = instrument_cost + accessories_cost
        self._logger.info(f"Рассчитана стоимость аренды #{self._rental_id}: {self._total_cost}")

    @check_permissions("can_rent")
    def rent_instrument(self) -> None:
        """Арендует инструмент, устанавливая его как недоступный."""
        self._instrument.rent_instrument()
        self._logger.info(f"Инструмент {self._instrument.name} арендован для {self._customer.name}")

    def generate_report(self) -> str:
        """Генерирует отчёт об аренде.

        Returns:
            Строковый отчёт об аренде.
        """
        accessories_str = ", ".join(str(acc) for acc in self._accessories) or "нет аксессуаров"
        report = (
            f"Отчет по аренде #{self._rental_id}:\n"
            f"Клиент: {self._customer.name}\n"
            f"Инструмент: {self._instrument.name}\n"
            f"Период: {self._start_date} - {self._end_date}\n"
            f"Аксессуары: {accessories_str}\n"
            f"Общая стоимость: {self._total_cost:.2f}"
        )
        self._logger.info(f"Сгенерирован отчет для аренды #{self._rental_id}")
        return report

    @classmethod
    def find_rental_by_id(cls, rental_id: UUID) -> 'Rental':
        """Находит аренду по её идентификатору.

        Args:
            rental_id: Идентификатор аренды.

        Returns:
            Объект аренды.

        Raises:
            RentalNotFoundError: Если аренда не найдена.
        """
        for rental in cls._rentals:
            if rental.rental_id == rental_id:
                return rental
        raise RentalNotFoundError(f"Аренда с ID {rental_id} не найдена")

    def to_dict(self) -> Dict:
        """Преобразует объект аренды в словарь.

        Returns:
            Словарь с данными об аренде.
        """
        return {
            'rental_id': str(self._rental_id),
            'customer': self._customer.to_dict(),
            'instrument': self._instrument.to_dict(),
            'start_date': self._start_date.isoformat(),
            'end_date': self._end_date.isoformat(),
            'accessories': [acc.to_dict() for acc in self._accessories],
            'total_cost': self._total_cost
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Rental':
        """Создаёт объект аренды из словаря.

        Args:
            data: Словарь с данными об аренде.

        Returns:
            Экземпляр аренды.
        """
        customer = Customer.from_dict(data['customer'])
        instrument = MusicalInstrument.from_dict(data['instrument'])
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
        rental = cls(customer, instrument, start_date, end_date)
        rental._rental_id = UUID(data['rental_id'])  # Восстанавливаем rental_id
        for acc_data in data.get('accessories', []):
            accessory = Accessory.from_dict(acc_data)
            rental._accessories.append(accessory)
        rental._total_cost = data['total_cost']
        rental.calculate_total()  # Пересчитываем для корректности
        return rental

    def __str__(self) -> str:
        """Возвращает строковое представление аренды.

        Returns:
            Строковое описание аренды.
        """
        return f"Аренда #{self._rental_id}: {self._customer.name} арендует {self._instrument.name}"