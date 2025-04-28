from .interfaces import RentalProcess
from .rental import Rental
import logging


class OnlineRentalProcess(RentalProcess):
    """Класс для управления процессом аренды инструментов онлайн."""

    def __init__(self):
        """Инициализирует процесс онлайн-аренды."""
        self._logger = logging.getLogger(self.__class__.__name__)

    def check_availability(self, rental: Rental) -> None:
        if not rental.instrument.is_available:
            raise ValueError(f"Инструмент {rental.instrument.name} недоступен для аренды")
        self._logger.info(f"Онлайн: Проверена доступность инструмента {rental.instrument.name}")

    def process_rental(self, rental: Rental) -> None:
        rental.rent_instrument()
        self._logger.info(f"Онлайн: Оформлена аренда #{rental.rental_id} для {rental.customer.name}")

    def confirm_rental(self, rental: Rental) -> None:
        rental.notify(f"Онлайн: Ваша аренда #{rental.rental_id} подтверждена для {rental.customer.email}")
        self._logger.info(f"Онлайн: Отправлено подтверждение аренды #{rental.rental_id} на {rental.customer.email}")


class OfflineRentalProcess(RentalProcess):
    """Класс для управления процессом аренды инструментов оффлайн."""

    def __init__(self):
        """Инициализирует процесс оффлайн-аренды."""
        self._logger = logging.getLogger(self.__class__.__name__)

    def check_availability(self, rental: Rental) -> None:
        if not rental.instrument.is_available:
            raise ValueError(f"Инструмент {rental.instrument.name} недоступен для аренды")
        self._logger.info(f"Оффлайн: Проверена доступность инструмента {rental.instrument.name}")

    def process_rental(self, rental: Rental) -> None:
        rental.rent_instrument()
        self._logger.info(f"Оффлайн: Оформлена аренда #{rental.rental_id} для {rental.customer.name}")

    def confirm_rental(self, rental: Rental) -> None:
        rental.notify(f"Оффлайн: Аренда #{rental.rental_id} подтверждена для {rental.customer.name} в офисе")
        self._logger.info(f"Оффлайн: Выдано подтверждение аренды #{rental.rental_id} для {rental.customer.name}")