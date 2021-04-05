import time
from concurrent.futures.thread import ThreadPoolExecutor
from threading import RLock
import telebot
from check_date import is_valid_date_and_time
import datetime
from datetime import timedelta

bot = telebot.TeleBot('')
list_of_tasks = []
lock = RLock()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    with lock:
        if message.text == "s":
            bot.send_message(message.from_user.id,
                             """
                             "Привет, добро пожаловать в Task manager!"
                             "Для создания списка дел введи  - 1"
                             "Для удаления задач введите - 2"
                             """)

        elif message.text == "1":
            bot.send_message(message.from_user.id, "Как тебя зовут ?")
            bot.register_next_step_handler(message, new_task)
        elif message.text == "2":
            bot.send_message(message.from_user.id, "Напиши, какую задачу вы хотите удалить ?")
            bot.register_next_step_handler(message, del_task)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши: s")


def new_task(message):
    list_of_tasks.append([])
    list_of_tasks[-1].append(message.from_user.id)
    print(list_of_tasks)
    list_of_tasks[-1].append(message.text)
    print(list_of_tasks)
    bot.send_message(message.from_user.id, "Что бы ты хотел что бы я напомнил ?")
    bot.register_next_step_handler(message, new_task2)


def new_task2(message):
    list_of_tasks[-1].append(message.text)
    print(list_of_tasks)
    bot.send_message(message.from_user.id, "Укажи дату и время, когда необходимо напомнить дд.мм.гггг.чч.мм ?")
    bot.register_next_step_handler(message, new_task3_valid)


def new_task3_valid(message):
    if is_valid_date_and_time(message.text) is not False:
        list_of_tasks[-1].append(message.text)
        bot.send_message(message.from_user.id, "За какое время напомнить 15, 30, 60, 120 минут ?")
        bot.register_next_step_handler(message, new_task4)
        print(list_of_tasks)
    else:
        bot.send_message(message.from_user.id, "Указано неверно, нужно в формате: дд.мм.гггг.чч.мм ?")
        bot.register_next_step_handler(message, new_task3_valid)


def new_task4(message):
    if message.text == "15" or message.text == "30" or message.text == "60" or message.text == "120":
        list_of_tasks[-1].append(message.text)
        bot.send_message(message.from_user.id, "Запомню :)")
        print(list_of_tasks)
    else:
        bot.send_message(message.from_user.id, "Введено неверно, напиши: 15, 30, 60, 120 ")
        bot.register_next_step_handler(message, new_task4)


def del_task(message):
    for i in reversed(range(len(list_of_tasks))):
        if list_of_tasks[i][2] == message.text:
            d = list_of_tasks[i]
            list_of_tasks.pop(i)
            bot.send_message(message.from_user.id, f'Задача {d} удалена')
            print(f'Задача {d} удалена')
            break
        else:
            bot.send_message(message.from_user.id, 'Задача не найдена')


def remind_worker():
    global list_of_tasks
    while True:
        try:
            print(list_of_tasks)
            with lock:
                for i in reversed(range(len(list_of_tasks))):
                    current_date = datetime.datetime.now()
                    remind_minutes = int(list_of_tasks[i][4])
                    remind_date = is_valid_date_and_time(list_of_tasks[i][3]) - timedelta(minutes=remind_minutes)
                    if current_date >= remind_date:
                        bot.send_message(list_of_tasks[i][0],
                                         f'{list_of_tasks[i][1]},  напоминаю: {list_of_tasks[i][2]}')
                        list_of_tasks.pop(i)

        except Exception as e:
            print("Ooops", e)
        time.sleep(10)


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(bot.polling, none_stop=True, interval=0)
        executor.submit(remind_worker)


if __name__ == "__main__":
    main()
