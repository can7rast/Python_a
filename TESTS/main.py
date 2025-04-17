from parser import parser
from test import test
import logging
import time


def main() :

    logger = logging.getLogger("Test logger")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('test.log', format('w'))
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        s = time.time()
        r = 0
        n = 0
        with open("test.txt", "r+") as f:
            questions = []
            parser(questions,f)
            n,r = test(questions ,logger)

        f = time.time()
        time_start = formatted_date = time.strftime("%d.%m.%Y", time.localtime(s)) + "  " + time.strftime("%H:%M:%S", time.localtime(s))
        time_finish = formatted_date = time.strftime("%d.%m.%Y", time.localtime(f)) + "  " + time.strftime("%H:%M:%S", time.localtime(f))


        try:
            logger.info(f"Время начала теста: {time_start}\n"
                    f"Время окончания теста: {time_finish}\n"
                    f"Общее количество вопросов: {n}\n"
                    f"Количество правильных ответов: {r}\n"
                    f"Процент правильных ответов: {r/n * 100:.2f}%\n")
        except ZeroDivisionError:
            logger.info(f"Время начала теста: {time_start}\n"
                        f"Время окончания теста: {time_finish}\n"
                        f"Общее количество вопросов: {n}\n"
                        f"Количество правильных ответов: {r}\n"
                        f"Процент правильных ответов:{0}%")
    except FileNotFoundError:
        print("Файл не найден!")
        logger.info(f"Ошибка! Файл не найден!")


if __name__ == "__main__":
    main()