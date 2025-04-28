from uuid import UUID, uuid4
from typing import Dict


class Accessory:
    """Класс для представления аксессуара к музыкальному инструменту."""

    def __init__(self, name: str, cost: float):
        """Инициализирует объект аксессуара.

        Args:
            name: Название аксессуара.
            cost: Стоимость аренды аксессуара за день.

        Raises:
            ValueError: Если название пустое или стоимость отрицательная.
        """
        self._accessory_id: UUID = uuid4()
        if not name.strip():
            raise ValueError("Название аксессуара не может быть пустым")
        if cost < 0:
            raise ValueError("Стоимость аксессуара не может быть отрицательной")
        self._name: str = name
        self._cost: float = cost

    @property
    def accessory_id(self) -> UUID:
        return self._accessory_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def cost(self) -> float:
        return self._cost

    def to_dict(self) -> Dict:
        return {
            'accessory_id': str(self._accessory_id),
            'name': self._name,
            'cost': self._cost
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Accessory':
        return cls(
            name=data['name'],
            cost=data['cost']
        )

    def __str__(self) -> str:
        return f"Аксессуар: {self._name}, Стоимость: {self._cost}"