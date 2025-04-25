from uuid import UUID, uuid4
from typing import Optional


class Customer:
    """Класс для представления клиента."""

    def __init__(self, name: str, email: str, phone: Optional[str] = None):
        """
        Args:
            name: Имя клиента.
            email: Электронная почта клиента.
            phone: Номер телефона клиента (опционально).
        """
        self._customer_id: UUID = uuid4()
        self._name: str = name
        self._email: str = email
        self._phone: Optional[str] = phone

    @property
    def customer_id(self) -> UUID:
        return self._customer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Имя клиента не может быть пустым")
        self._name = value

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value or "." not in value:
            raise ValueError("Некорректный формат электронной почты")
        self._email = value

    @phone.setter
    def phone(self, value: Optional[str]) -> None:
        self._phone = value

    def __str__(self) -> str:
        return f"Клиент: {self._name}, Email: {self._email}, Телефон: {self._phone or 'не указан'}"