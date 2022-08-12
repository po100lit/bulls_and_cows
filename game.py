import random


# Проверяем на повторяющиеся цифры: True, если повторов нет
def noDuplicates(num):
    num_li = getDigits(num)
    if len(num_li) == len(set(num_li)):
        return True
    else:
        return False


# Создаём список из цифр числа
def getDigits(num):
    return [int(i) for i in str(num)]


# Генерируем четырехзначное число
def generateNum():
    while True:
        num = random.randint(1000, 9999)
        if noDuplicates(num):
            # print(num)  # показывает загаданное компьютером число
            return num


num = generateNum()
tries = int(input("Введите количество попыток: "))


# Поиск быков и коров
def numOfBullsCows(num, guess):
    bull_cow = [0, 0]
    num_li = getDigits(num)
    guess_li = getDigits(guess)
    for i, j in zip(num_li, guess_li):
        # есть ли цифра в списке
        if j in num_li:
            # цифра есть и стоит на своём месте
            if j == i:
                bull_cow[0] += 1
            # цифра есть, но стоит не на своём месте
            else:
                bull_cow[1] += 1
    return bull_cow


# Играем пока не кончатся попытки или не угадаем число
while tries > 0:
    guess = int(input("Введите число: "))
    if not noDuplicates(guess):
        print("Цифры не должны повторяться")
        continue
    if guess < 1000 or guess > 9999:
        print("Загаданное число состоит из 4 цифр")
        continue
    bull_cow = numOfBullsCows(num, guess)
    print(f"{bull_cow[0]} бык(а), {bull_cow[1]} корова(ы)")
    tries -= 1
    if bull_cow[0] == 4:
        print("Поздравляю! Вы угадали!")
        break
else:
    print(f"У вас кончились попытки. Было загадано число {num}")


def main():
    pass


if __name__ == '__main__':
    main()
