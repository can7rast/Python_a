class InstrumentFactory:
    """Фабрика для создания музыкальных инструментов."""

    @staticmethod
    def create_instrument(instrument_type: str, *args, **kwargs):
        """Создаёт экземпляр инструмента по типу.

        Args:
            instrument_type: Тип инструмента ("guitar", "piano", "violin").
            *args, **kwargs: Аргументы для инициализации инструмента.
        Returns:
            Экземпляр класса инструмента.
        Raises:
            ValueError: Если тип инструмента неизвестен.
        """
        from instruments import Guitar, Piano, Violin  # Отложенный импорт

        instrument_classes = {
            "guitar": Guitar,
            "piano": Piano,
            "violin": Violin
        }

        instrument_class = instrument_classes.get(instrument_type.lower())
        if not instrument_class:
            raise ValueError(f"Неизвестный тип инструмента: {instrument_type}")
        return instrument_class(*args, **kwargs)