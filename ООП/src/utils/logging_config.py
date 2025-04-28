import logging
import os
from datetime import datetime

def setup_logging():
    """Настраивает систему логирования для записи в файл и вывода в консоль."""
    # Создаём папку logs, если она не существует
    os.makedirs("logs", exist_ok=True)

    # Формируем имя файла логов с текущей датой
    log_filename = f"logs/rental_service_{datetime.now().strftime('%Y%m%d')}.log"

    # Настраиваем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Создаём и настраиваем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Удаляем существующие обработчики, чтобы избежать дублирования
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Обработчик для файла
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger