from random import shuffle
from answer import answer

def test(arr,logger):
    shuffle(arr)
    for i in range(len(arr)):
        shuffle(arr[i][1])
    try:
        n = int(input("Введите кол-во вопросов:"))
    except ValueError:
        logger.info("Ошибка ввода количества вопросов!")
        exit(1)

    #Кол-во вопросов
    current_answers = 0

    #Бежим по вопросам по одному
    k = 1
    for i in range(n):
        print(arr[i][0])
        print("Варианты ответов:")
        for j in arr[i][1]:
            print(str(k) + ".",j, sep= " ")
            k = k + 1
            if k % 6 == 0:
                k = 1
        ans = ""
        ans = input("Введите ответ:")
        if ans not in "12345":
            ans = answer(ans)
        if arr[i][1][int(ans) - 1] == arr[i][2]:
            print("Правильно!")
            current_answers += 1
        else:
            print("Неверно!")

    return n, current_answers

