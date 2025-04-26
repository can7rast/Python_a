from uuid import UUID, uuid4
from typing import Optional, List

class Customer:
    """Класс для представления клиента."""

    def __init__(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        permissions: Optional[List[str]] = None
    ):
        """
        Args:
            name: Имя клиента.
            email: Электронная почта клиента.
            phone: Номер телефона клиента (опционально).
            permissions: Список разрешений клиента (опционально).
        """
        self._customer_id: UUID = uuid4()
        self._name: str = name
        self._email: str = email
        self._phone: Optional[str] = phone
        self._permissions: List[str] = permissions if permissions is not None else []
        # Валидация при инициализации
        self.name = name  # Используем сеттер для валидации
        self.email = email  # Используем сеттер для валидации

    @property
    def customer_id(self) -> UUID:
        """Возвращает идентификатор клиента."""
        return self._customer_id

    @property
    def name(self) -> str:
        """Возвращает имя клиента."""
        return self._name

    @property
    def email(self) -> str:
        """Возвращает электронную почту клиента."""
        return self._email

    @property
    def phone(self) -> Optional[str]:
        """Возвращает номер телефона клиента."""
        return self._phone

    @property
    def permissions(self) -> List[str]:
        """Возвращает список разрешений клиента."""
        return self._permissions

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя клиента."""
        if not value.strip():
            raise ValueError("Имя клиента не может быть пустым")
        self._name = value

    @email.setter
    def email(self, value: str) -> None:
        """Устанавливает электронную почту клиента."""
        if "@" not in value or "." not in value:
            raise ValueError("Некорректный формат электронной почты")
        self._email = value

    @phone.setter
    def phone(self, value: Optional[str]) -> None:
        """Устанавливает номер телефона клиента."""
        self._phone = value

    @permissions.setter
    def permissions(self, value: List[str]) -> None:
        """Устанавливает список разрешений клиента."""
        if not isinstance(value, list) or not all(isinstance(p, str) for p in value):
            raise ValueError("Разрешения должны быть списком строк")
        self._permissions = value

    def __str__(self) -> str:
        """Возвращает строковое представление клиента."""
        return f"Клиент: {self._name}, Email: {self._email}, Телефон: {self._phone or 'не указан'}"