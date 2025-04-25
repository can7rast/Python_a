from enum import Enum
from .interfaces import RentalRequestHandler

class RequestType(Enum):
    SIMPLE = "simple"
    DISCOUNT = "discount"
    COMPLEX = "complex"

class RentalRequest:
    """Класс, представляющий запрос на аренду."""

    def __init__(self, request_type: RequestType, amount: float, description: str):
        """Инициализация запроса.

        Args:
            request_type: Тип запроса (simple, discount, complex).
            amount: Сумма запроса.
            description: Описание запроса.
        """
        self.request_type = request_type
        self.amount = amount
        self.description = description

class Operator(RentalRequestHandler):
    """Обработчик простых запросов."""

    def handle_request(self, request: RentalRequest) -> str:
        if request.request_type == RequestType.SIMPLE:
            return f"Оператор обработал простой запрос: {request.description} (сумма: {request.amount})"
        elif self._successor:
            return self._successor.handle_request(request)
        return f"Оператор не может обработать запрос: {request.description}"

class Manager(RentalRequestHandler):
    """Обработчик запросов на скидки."""

    def handle_request(self, request: RentalRequest) -> str:
        if request.request_type == RequestType.DISCOUNT:
            return f"Менеджер обработал запрос на скидку: {request.description} (сумма: {request.amount})"
        elif self._successor:
            return self._successor.handle_request(request)
        return f"Менеджер не может обработать запрос: {request.description}"

class Admin(RentalRequestHandler):
    """Обработчик сложных запросов."""

    def handle_request(self, request: RentalRequest) -> str:
        if request.request_type == RequestType.COMPLEX:
            return f"Админ обработал сложный запрос: {request.description} (сумма: {request.amount})"
        return f"Админ не может обработать запрос: {request.description}"