from uuid import UUID, uuid4
from typing import Optional


class Accessory:
    def __init__(self, name: str, cost: float):
        """
        Args:
            name: Название аксессуара.
            cost: Стоимость аксессуара за аренду.
        """
        self._accessory_id: UUID = uuid4()
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

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Название аксессуара не может быть пустым")
        self._name = value

    @cost.setter
    def cost(self, value: float) -> None:
        if value < 0:
            raise ValueError("Стоимость аксессуара не может быть отрицательной")
        self._cost = value

    def __str__(self) -> str:
        return f"Аксессуар: {self._name}, Стоимость: {self._cost}"