class InstrumentMeta(type):
    """Метакласс для автоматической регистрации подклассов MusicalInstrument."""

    _registry = {}  # Реестр: имя класса -> класс

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name != 'MusicalInstrument':  # Не регистрируем базовый класс
            cls._registry[name] = new_class
        return new_class

    @classmethod
    def get_registered_classes(cls):
        return cls._registry

    @classmethod
    def create_instrument(cls, instrument_type: str, *args, **kwargs):
        instrument_class = cls._registry.get(instrument_type)
        if not instrument_class:
            raise ValueError(f"Инструмент типа '{instrument_type}' не зарегистрирован")
        return instrument_class(*args, **kwargs)