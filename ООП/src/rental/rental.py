from uuid import UUID, uuid4
from datetime import datetime, date
from typing import List, Optional
from .customer import Customer
from .accessory import Accessory
from instruments.musical_instrument import MusicalInstrument
from .interfaces import Rentable, Reportable
from utils import LoggingMixin, NotificationMixin

class Rental(Rentable, Reportable, LoggingMixin, NotificationMixin):
    """Класс для представления аренды."""

    def __init__(
            self,
            customer: Customer,
            instrument: MusicalInstrument,
            start_date: date,
            end_date: date
    ):
        """Инициализация аренды.

        Args:
            customer: Клиент, арендующий инструмент.
            instrument: Музыкальный инструмент.
            start_date: Дата начала аренды.
            end_date: Дата окончания аренды.
        """
        self._rental_id: UUID = uuid4()
        self._customer: Customer = customer
        self._instrument: MusicalInstrument = instrument
        self._start_date: date = start_date
        self._end_date: date = end_date
        self._accessories: List[Accessory] = []
        self._total_cost: float = 0.0
        self.calculate_total()
        self.log_action(f"Создана аренда #{self._rental_id} для {customer.name}")
        self.send_notification(
            f"Ваш инструмент {instrument.name} готов к выдаче",
            customer.email
        )

    @property
    def rental_id(self) -> UUID:
        """Возвращает идентификатор аренды."""
        return self._rental_id

    @property
    def customer(self) -> Customer:
        """Возвращает клиента."""
        return self._customer

    @property
    def instrument(self) -> MusicalInstrument:
        """Возвращает инструмент."""
        return self._instrument

    @property
    def start_date(self) -> date:
        """Возвращает дату начала аренды."""
        return self._start_date

    @property
    def end_date(self) -> date:
        """Возвращает дату окончания аренды."""
        return self._end_date

    @property
    def total_cost(self) -> float:
        """Возвращает общую стоимость аренды."""
        return self._total_cost

    @property
    def accessories(self) -> List[Accessory]:
        """Возвращает список аксессуаров."""
        return self._accessories

    def add_accessory(self, accessory: Accessory) -> None:
        """Добавляет аксессуар к аренде.

        Args:
            accessory: Аксессуар для добавления.
        """
        self._accessories.append(accessory)
        self.calculate_total()
        self.log_action(f"Добавлен аксессуар {accessory.name} к аренде #{self._rental_id}")

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
                self.log_action(f"Удален аксессуар {accessory.name} из аренды #{self._rental_id}")
                return
        raise ValueError("Аксессуар не найден")

    def calculate_total(self) -> None:
        """Рассчитывает общую стоимость аренды."""
        days = (self._end_date - self._start_date).days
        if days <= 0:
            self._total_cost = 0.0
            return
        instrument_cost = self._instrument.calculate_rental_cost(days)
        accessories_cost = sum(accessory.cost * days for accessory in self._accessories)
        self._total_cost = instrument_cost + accessories_cost
        self.log_action(f"Рассчитана стоимость аренды #{self._rental_id}: {self._total_cost}")

    def rent_instrument(self) -> None:
        """Арендует инструмент, устанавливая его как недоступный."""
        if not self._instrument.is_available:
            raise ValueError("Инструмент уже арендован")
        self._instrument.is_available = False
        self.log_action(f"Инструмент {self._instrument.name} арендован для {self._customer.name}")
        self.send_notification(
            f"Аренда инструмента {self._instrument.name} подтверждена",
            self._customer.email
        )

    def generate_report(self) -> str:
        """Генерирует отчет об аренде.

        Returns:
            Строковое представление отчета.
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
        self.log_action(f"Сгенерирован отчет для аренды #{self._rental_id}")
        return report

    def __str__(self) -> str:
        """Возвращает строковое представление аренды."""
        return f"Аренда #{self._rental_id}: {self._customer.name} арендует {self._instrument.name}"