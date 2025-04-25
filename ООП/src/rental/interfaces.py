from abc import ABC, abstractmethod
from typing import Optional

class Rentable(ABC):
    @abstractmethod
    def rent_instrument(self) -> None:
        pass

class Reportable(ABC):
    @abstractmethod
    def generate_report(self) -> str:
        pass

class RentalRequestHandler(ABC):
    """Абстрактный класс для обработки запросов на аренду."""

    def __init__(self, successor: Optional['RentalRequestHandler'] = None):
        """Инициализация обработчика с указанием следующего в цепочке.

        Args:
            successor: Следующий обработчик в цепочке.
        """
        self._successor = successor

    @abstractmethod
    def handle_request(self, request: 'RentalRequest') -> str:
        """Обрабатывает запрос или передаёт следующему обработчику.

        Args:
            request: Запрос на аренду.
        Returns:
            Результат обработки запроса.
        """
        pass

class RentalProcess(ABC):
    """Абстрактный класс для процесса аренды инструмента."""

    def rent_instrument(self, rental: 'Rental') -> None:
        """Шаблонный метод для процесса аренды.

        Args:
            rental: Объект аренды.
        """
        self.check_availability(rental)
        self.process_rental(rental)
        self.confirm_rental(rental)

    @abstractmethod
    def check_availability(self, rental: 'Rental') -> None:
        """Проверяет доступность инструмента."""
        pass

    @abstractmethod
    def process_rental(self, rental: 'Rental') -> None:
        """Оформляет аренду."""
        pass

    @abstractmethod
    def confirm_rental(self, rental: 'Rental') -> None:
        """Подтверждает аренду."""
        pass