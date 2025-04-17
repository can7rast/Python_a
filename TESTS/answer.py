def answer(ans):
    print("Вы ввели некорректный ответ!")
    n = input("Введите ответ:")
    if n in "12345":
        return n
    else:
        answer(ans)