from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import os
from game import *

token = os.getenv('TOKEN')
updater = Updater(token)
dispatcher = updater.dispatcher

guess = None
PLAYER, MOVE = 0, 1
player_name = None

print('Бот работает...')


def start(update, context):
    global num, count
    num = generate_num()  # "загадываем" число
    count = 1
    print(num)  # для тестирования выводим число в консоль
    context.bot.send_message(update.effective_chat.id,
                             f'Привет! Сыграем в "Быки и Коровы"?\n'
                             f'Правила просты и доступны по <a href="https://bit.ly/3bVRJMr">ссылке</a>',
                             parse_mode='HTML', disable_web_page_preview=True)
    context.bot.send_sticker(update.effective_chat.id,
                             'CAACAgIAAxkBAAEFjQ5i97CjfmC2zqTc1a-w07yiD57T5QACYwQAApzW5wrqBq1QxVaLyikE')
    context.bot.send_message(update.effective_chat.id, 'Меня зовут Джон Крамер, а тебя?')
    return PLAYER


def get_name(update, context):
    global player_name, count
    player_name = update.message.text
    src_gif = open('src/saw.mp4', 'rb')
    context.bot.send_message(update.effective_chat.id, 'Игра началась... <b>У тебя есть 10 попыток...</b>',
                             parse_mode='HTML')
    context.bot.send_video(update.effective_chat.id, src_gif)
    context.bot.send_message(update.effective_chat.id, 'Введи число...')
    context.bot.send_message(update.effective_chat.id, f'Попытка {count}...')
    return MOVE


def take_move(update, context):
    global guess, count
    try:
        guess = int(update.message.text)
    except:
        context.bot.send_message(update.effective_chat.id, f'Введи число...')
        return MOVE
    if not check_duplicates(guess):
        context.bot.send_message(update.effective_chat.id, f'В загаданном числе цифры не повторяются')
        return MOVE
    if guess < 1000 or guess > 9999:
        context.bot.send_message(update.effective_chat.id, f'Загаданное число состоит из 4 цифр')
        return MOVE
    count += 1  # увеличиваем счетчик попыток !!! обязательно после проверок ввода
    bull_cow = bulls_and_cows(num, guess)
    if bull_cow[0] == 4:  # если быков 4 - выигрыш
        context.bot.send_message(update.effective_chat.id,
                                 f'Браво, {player_name}! Число {num} отгадано за {count - 1} попыток')
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFjfVi9-4HMKO0m66wSCeFS1vsXtVbWwACgxgAAstUsErrON6r0Zh6GSkE')
        return ConversationHandler.END
    if count <= 10:  # используем попытки
        context.bot.send_message(update.effective_chat.id, f'быков - {bull_cow[0]} | коров - {bull_cow[1]}')
        context.bot.send_message(update.effective_chat.id, f'Попытка {count}...')
        return MOVE
    else:  # если попыток больше 10 - проигрыш
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFjdli9-TCSwTMPiIuJyaQV3-oXwjJHgACThQAAjTTYEjImOUXwyoZhSkE')
        context.bot.send_message(update.effective_chat.id,
                                 f'Увы, {player_name}, ты потратил свои {count - 1} попыток и проиграл...')
        context.bot.send_message(update.effective_chat.id,
                                 f'В интернете есть описание нескольких выигрышных стратегий для этой игры =)\n'
                                 f'Советую почитать! Жду тебя снова =)')
        return ConversationHandler.END


def exit(update, context):
    context.bot.send_message(update.effective_chat.id, 'Game over')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PLAYER: [MessageHandler(Filters.text, get_name)],
        MOVE: [MessageHandler(Filters.text, take_move)]
    },
    fallbacks=[CommandHandler('exit', exit)])

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
print('Бот отключен!')
