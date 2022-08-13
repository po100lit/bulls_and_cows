import random


# Проверяем на повторяющиеся цифры: True, если повторов нет
def check_duplicates(num: int) -> bool:
    num_li = get_digits(num)
    return len(num_li) == len(set(num_li))


# Создаём список из цифр числа
def get_digits(num: int) -> list:
    return [int(i) for i in str(num)]


# Генерируем четырехзначное число
def generate_num() -> int:
    while True:
        num = random.randint(1000, 9999)
        if check_duplicates(num):
            return num


# Поиск быков и коров
def bulls_and_cows(num: int, guess: int) -> list[int]:
    bull_cow = [0, 0]
    num_list = get_digits(num)
    guess_list = get_digits(guess)
    for i, j in zip(num_list, guess_list):
        if j in num_list:  # есть ли цифра в списке
            if j == i:  # цифра есть и стоит на своём месте
                bull_cow[0] += 1
            else:  # цифра есть, но стоит не на своём месте
                bull_cow[1] += 1
    return bull_cow
