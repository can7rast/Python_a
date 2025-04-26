from instruments import MusicalInstrument, Guitar, Piano, Violin, InstrumentMeta
from rental import Customer, Accessory, Rental, RentalRequest, RequestType, Operator, Manager, Admin, \
    OnlineRentalProcess, OfflineRentalProcess
from utils import InstrumentFactory, PermissionDeniedError
from datetime import date, timedelta


def main():
    try:
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
        print(customer_with_permissions)
        print(customer_without_permissions)

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
        print(guitar)
        print(piano)
        print(violin)

        # Демонстрация метакласса: создание инструментов по имени типа
        print("\nДемонстрация метакласса:")
        guitar2 = MusicalInstrument.create_instrument(
            "guitar", name="Gibson Les Paul", condition="new", daily_rate=60.0, number_of_strings=6
        )
        piano2 = MusicalInstrument.create_instrument(
            "piano", name="Steinway D", condition="refurbished", daily_rate=150.0, key_count=88
        )
        violin2 = MusicalInstrument.create_instrument(
            "violin", name="Amati Copy", condition="used", daily_rate=70.0, bow_included=False
        )
        print(guitar2)
        print(piano2)
        print(violin2)

        # Демонстрация фабрики: создание дополнительных инструментов
        print("\nДемонстрация фабрики:")
        guitar3 = InstrumentFactory.create_instrument(
            "guitar", name="Ibanez RG", condition="used", daily_rate=45.0, number_of_strings=7
        )
        print(guitar3)

        # Создание аксессуара
        case = Accessory(name="Гитарный чехол", cost=5.0)
        print(case)

        # Создание аренд
        start_date = date.today()
        end_date = start_date + timedelta(days=10)

        # Онлайн-аренда (с правами)
        print("\nОнлайн-аренда (с правами):")
        online_rental = Rental(
            customer=customer_with_permissions,
            instrument=guitar,
            start_date=start_date,
            end_date=end_date
        )
        online_rental.add_accessory(case)
        print(online_rental)
        online_process = OnlineRentalProcess()
        online_process.rent_instrument(online_rental)
        print(f"Инструмент после онлайн-аренды: {guitar}")
        print(online_rental.generate_report())

        # Онлайн-аренда (без прав)
        print("\nОнлайн-аренда (без прав):")
        try:
            unauthorized_rental = Rental(
                customer=customer_without_permissions,
                instrument=violin,
                start_date=start_date,
                end_date=end_date
            )
            online_process.rent_instrument(unauthorized_rental)
        except PermissionDeniedError as e:
            print(f"Ошибка доступа: {e}")

        # Оффлайн-аренда
        print("\nОффлайн-аренда:")
        offline_rental = Rental(
            customer=customer_with_permissions,
            instrument=piano,
            start_date=start_date,
            end_date=end_date
        )
        offline_rental.add_accessory(case)
        print(offline_rental)
        offline_process = OfflineRentalProcess()
        offline_process.rent_instrument(offline_rental)
        print(f"Инструмент после оффлайн-аренды: {piano}")
        print(offline_rental.generate_report())

        # Проверка обработки ошибок
        print("\nПроверка удаления аксессуара:")
        try:
            online_rental.remove_accessory(case.accessory_id)
            online_rental.remove_accessory(case.accessory_id)  # Ошибка: аксессуар уже удалён
        except ValueError as e:
            print(f"Ошибка: {e}")

        # Демонстрация цепочки обязанностей
        print("\nДемонстрация цепочки обязанностей:")
        admin = Admin()
        manager = Manager(successor=admin)
        operator = Operator(successor=manager)

        # Создание запросов
        simple_request = RentalRequest(RequestType.SIMPLE, 100.0, "Аренда гитары")
        discount_request = RentalRequest(RequestType.DISCOUNT, 50.0, "Скидка на аренду пианино")
        complex_request = RentalRequest(RequestType.COMPLEX, 1000.0, "Специальный заказ скрипки")

        # Обработка запросов
        print(operator.handle_request(simple_request))
        print(operator.handle_request(discount_request))
        print(operator.handle_request(complex_request))

        # Проверка реестра метакласса
        print("\nЗарегистрированные классы инструментов:")
        print(InstrumentMeta.get_registered_classes())

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()