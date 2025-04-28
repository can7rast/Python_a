class PermissionDeniedError(Exception):
    """Исключение, возникающее при отсутствии прав доступа."""
    pass

class InvalidInstrumentError(Exception):
    """Исключение, возникающее при некорректных данных инструмента."""
    pass

class RentalNotFoundError(Exception):
    """Исключение, возникающее при отсутствии аренды."""
    pass