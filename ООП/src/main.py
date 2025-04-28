from instruments import MusicalInstrument, Guitar, Piano, Violin, InstrumentMeta
from rental import Customer, Accessory, Rental, RentalRequest, RequestType, Operator, Manager, Admin, OnlineRentalProcess, OfflineRentalProcess
from utils import InstrumentFactory, PermissionDeniedError, InvalidInstrumentError, RentalNotFoundError
from utils.serialization import save_to_json, load_from_json
from utils.logging_config import setup_logging
from datetime import date, timedelta
from uuid import UUID
import logging

def main():
    """Основная функция программы, демонстрирующая функциональность системы аренды инструментов."""
    try:
        # Настройка логирования
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Программа запущена")

        # Создание клиентов
        customer_with_permissions = Customer(
            name="Иван Иванов",
            email="ivan@example.com",
            phone="+79991234567",
            permissions=["can_rent", "can_modify_rental"]
        )
        customer_without_permissions = Customer(
            name="Пётр Петров",
            email="petr@example.com",
            phone="+79997654321",
            permissions=[]
        )
        print(customer_with_permissions, flush=True)
        print(customer_without_permissions, flush=True)

        # Демонстрация InvalidInstrumentError
        print("\nПроверка InvalidInstrumentError:", flush=True)
        try:
            invalid_guitar = Guitar(
                name="", condition="new", daily_rate=50.0, number_of_strings=6
            )
        except InvalidInstrumentError as e:
            logger.error(f"Ошибка инструмента: {e}")
            print(f"Ошибка инструмента: {e}", flush=True)
        try:
            invalid_piano = Piano(
                name="Yamaha", condition="new", daily_rate=-10.0, key_count=88
            )
        except InvalidInstrumentError as e:
            logger.error(f"Ошибка инструмента: {e}")
            print(f"Ошибка инструмента: {e}", flush=True)
        try:
            guitar = Guitar("Fender", "new", 50.0, 6)
            guitar.condition = "invalid"
        except InvalidInstrumentError as e:
            logger.error(f"Ошибка инструмента (сеттер): {e}")
            print(f"Ошибка инструмента (сеттер): {e}", flush=True)

        # Создание инструментов через фабрику
        guitar = InstrumentFactory.create_instrument(
            "guitar", name="Fender Stratocaster", condition="new", daily_rate=50.0, number_of_strings=6
        )
        piano = InstrumentFactory.create_instrument(
            "piano", name="Yamaha U1", condition="used", daily_rate=100.0, key_count=88
        )
        violin = InstrumentFactory.create_instrument(
            "violin", name="Stradivarius Copy", condition="refurbished", daily_rate=80.0, bow_included=True
        )

        # Проверка строкового представления
        print(guitar, flush=True)
        print(piano, flush=True)
        print(violin, flush=True)

        # Демонстрация методов сравнения
        print("\nДемонстрация методов сравнения:", flush=True)
        guitar_same = InstrumentFactory.create_instrument(
            "guitar", name="Fender Copy", condition="new", daily_rate=50.0, number_of_strings=6
        )
        guitar_different = InstrumentFactory.create_instrument(
            "guitar", name="Gibson", condition="used", daily_rate=50.0, number_of_strings=6
        )
        print(f"Сравнение guitar == guitar_same: {guitar == guitar_same}", flush=True)
        print(f"Сравнение guitar == guitar_different: {guitar == guitar_different}", flush=True)
        print(f"Сравнение guitar < piano: {guitar < piano}", flush=True)
        print(f"Сравнение violin > guitar: {violin > guitar}", flush=True)
        print(f"Сравнение guitar_different < guitar: {guitar_different < guitar}", flush=True)

        # Демонстрация метакласса
        print("\nДемонстрация метакласса:", flush=True)
        guitar2 = MusicalInstrument.create_instrument(
            "guitar", name="Gibson Les Paul", condition="new", daily_rate=60.0, number_of_strings=6
        )
        piano2 = MusicalInstrument.create_instrument(
            "piano", name="Steinway D", condition="refurbished", daily_rate=150.0, key_count=88
        )
        violin2 = MusicalInstrument.create_instrument(
            "violin", name="Amati Copy", condition="used", daily_rate=70.0, bow_included=False
        )
        print(guitar2, flush=True)
        print(piano2, flush=True)
        print(violin2, flush=True)

        # Демонстрация фабрики
        print("\nДемонстрация фабрики:", flush=True)
        guitar3 = InstrumentFactory.create_instrument(
            "guitar", name="Ibanez RG", condition="used", daily_rate=45.0, number_of_strings=7
        )
        print(guitar3, flush=True)

        # Создание аксессуара
        case = Accessory(name="Гитарный чехол", cost=5.0)
        print(case, flush=True)

        # Создание аренд
        start_date = date.today()
        end_date = start_date + timedelta(days=10)

        # Проверка валидации дат
        print("\nПроверка валидации дат:", flush=True)
        try:
            invalid_rental = Rental(
                customer=customer_with_permissions,
                instrument=guitar,
                start_date=end_date,
                end_date=start_date
            )
        except ValueError as e:
            logger.error(f"Ошибка дат аренды: {e}")
            print(f"Ошибка дат аренды: {e}", flush=True)

        # Онлайн-аренда (с правами)
        print("\nОнлайн-аренда (с правами):", flush=True)
        online_rental = Rental(
            customer=customer_with_permissions,
            instrument=guitar,
            start_date=start_date,
            end_date=end_date
        )
        online_rental.add_accessory(case)
        print(online_rental, flush=True)
        online_process = OnlineRentalProcess()
        online_process.rent_instrument(online_rental)
        print(f"Инструмент после онлайн-аренды: {guitar}", flush=True)
        print(online_rental.generate_report(), flush=True)

        # Онлайн-аренда (без прав)
        print("\nОнлайн-аренда (без прав):", flush=True)
        try:
            unauthorized_rental = Rental(
                customer=customer_without_permissions,
                instrument=violin,
                start_date=start_date,
                end_date=end_date
            )
            online_process.rent_instrument(unauthorized_rental)
        except PermissionDeniedError as e:
            logger.error(f"Ошибка доступа: {e}")
            print(f"Ошибка доступа: {e}", flush=True)

        # Оффлайн-аренда
        print("\nОффлайн-аренда:", flush=True)
        offline_rental = Rental(
            customer=customer_with_permissions,
            instrument=piano,
            start_date=start_date,
            end_date=end_date
        )
        offline_rental.add_accessory(case)
        print(offline_rental, flush=True)
        offline_process = OfflineRentalProcess()
        offline_process.rent_instrument(offline_rental)
        print(f"Инструмент после оффлайн-аренды: {piano}", flush=True)
        print(offline_rental.generate_report(), flush=True)

        # Демонстрация RentalNotFoundError
        print("\nПроверка RentalNotFoundError:", flush=True)
        try:
            non_existent_rental = Rental.find_rental_by_id(UUID("00000000-0000-0000-0000-000000000000"))
        except RentalNotFoundError as e:
            logger.error(f"Ошибка аренды: {e}")
            print(f"Ошибка аренды: {e}", flush=True)

        # Проверка удаления аксессуара
        print("\nПроверка удаления аксессуара:", flush=True)
        try:
            online_rental.remove_accessory(case.accessory_id)
            online_rental.remove_accessory(case.accessory_id)  # Ошибка: аксессуар уже удалён
        except ValueError as e:
            logger.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}", flush=True)

        # Демонстрация цепочки обязанностей
        print("\nДемонстрация цепочки обязанностей:", flush=True)
        admin = Admin()
        manager = Manager(successor=admin)
        operator = Operator(successor=manager)

        # Создание запросов
        simple_request = RentalRequest(RequestType.SIMPLE, 100.0, "Аренда гитары")
        discount_request = RentalRequest(RequestType.DISCOUNT, 50.0, "Скидка на аренду пианино")
        complex_request = RentalRequest(RequestType.COMPLEX, 1000.0, "Специальный заказ скрипки")

        # Обработка запросов
        print(operator.handle_request(simple_request), flush=True)
        print(operator.handle_request(discount_request), flush=True)
        print(operator.handle_request(complex_request), flush=True)

        # Проверка реестра метакласса
        print("\nЗарегистрированные классы инструментов:", flush=True)
        print(InstrumentMeta.get_registered_classes(), flush=True)

        # Демонстрация сериализации и десериализации
        print("\nДемонстрация сериализации и десериализации:", flush=True)
        instruments = [guitar, piano, violin, guitar2, piano2, violin2, guitar3]
        rentals = [online_rental, offline_rental]
        save_to_json(instruments, rentals, "data/rental_data.json")
        print("Данные сохранены в data/rental_data.json", flush=True)

        loaded_instruments, loaded_rentals = load_from_json("data/rental_data.json")
        print(f"Загружено инструментов: {len(loaded_instruments)}", flush=True)
        print(f"Загружено аренд: {len(loaded_rentals)}", flush=True)
        for inst in loaded_instruments:
            print(inst, flush=True)
        for rental in loaded_rentals:
            print(rental.generate_report(), flush=True)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}", flush=True)

if __name__ == "__main__":
    main()