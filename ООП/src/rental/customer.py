from typing import Optional, List, Dict
from uuid import UUID, uuid4


class Customer:
    """Класс для представления клиента, арендующего инструменты."""

    def __init__(self, name: str, email: str, phone: Optional[str] = None, permissions: Optional[List[str]] = None):
        """Инициализирует объект клиента.

        Args:
            name: Имя клиента.
            email: Электронная почта клиента.
            phone: Телефон клиента (опционально).
            permissions: Список разрешений клиента (опционально).
        """
        self._customer_id: UUID = uuid4()
        self._name: str = name
        self._email: str = email
        self._phone: Optional[str] = phone
        self._permissions: List[str] = permissions or []

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

    @property
    def permissions(self) -> List[str]:
        return self._permissions

    def has_permission(self, permission: str) -> bool:
        return permission in self._permissions

    def to_dict(self) -> Dict:
        return {
            'customer_id': str(self._customer_id),
            'name': self._name,
            'email': self._email,
            'phone': self._phone,
            'permissions': self._permissions
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':

        return cls(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            permissions=data.get('permissions', [])
        )

    def __str__(self) -> str:
        return f"Клиент: {self._name}, Email: {self._email}, Телефон: {self._phone or 'не указан'}"