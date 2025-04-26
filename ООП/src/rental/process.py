from .interfaces import RentalProcess
from .rental import Rental
from utils import LoggingMixin

class OnlineRentalProcess(RentalProcess, LoggingMixin):
    """Процесс аренды инструмента онлайн."""

    def __init__(self):
        LoggingMixin.__init__(self)

    def check_availability(self, rental: Rental) -> None:
        if not rental.instrument.is_available:
            raise ValueError(f"Инструмент {rental.instrument.name} недоступен для аренды")
        self.log(f"Онлайн: Проверена доступность инструмента {rental.instrument.name}")

    def process_rental(self, rental: Rental) -> None:
        rental.rent_instrument()
        self.log(f"Онлайн: Оформлена аренда #{rental.rental_id} для {rental.customer.name}")

    def confirm_rental(self, rental: Rental) -> None:
        rental.notify(f"Онлайн: Ваша аренда #{rental.rental_id} подтверждена для {rental.customer.email}")
        self.log(f"Онлайн: Отправлено подтверждение аренды #{rental.rental_id} на {rental.customer.email}")

class OfflineRentalProcess(RentalProcess, LoggingMixin):
    """Процесс аренды инструмента оффлайн."""

    def __init__(self):
        LoggingMixin.__init__(self)

    def check_availability(self, rental: Rental) -> None:
        if not rental.instrument.is_available:
            raise ValueError(f"Инструмент {rental.instrument.name} недоступен для аренды")
        self.log(f"Оффлайн: Проверена доступность инструмента {rental.instrument.name}")

    def process_rental(self, rental: Rental) -> None:
        rental.rent_instrument()
        self.log(f"Оффлайн: Оформлена аренда #{rental.rental_id} для {rental.customer.name}")

    def confirm_rental(self, rental: Rental) -> None:
        rental.notify(f"Оффлайн: Аренда #{rental.rental_id} подтверждена для {rental.customer.name} в офисе")
        self.log(f"Оффлайн: Выдано подтверждение аренды #{rental.rental_id} для {rental.customer.name}")