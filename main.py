import sqlite3
import telebot
from telebot import types
import config

bot = telebot.TeleBot("TOKEN")

conn = sqlite3.connect('tasks.sqlite', check_same_thread=False)
cursor = conn.cursor()
chapters_str = ''
sub_chapters_str = ''
level_str = ''
tasks_str = ''
chapter_id = ''
sub_chapter_id = ''
level_id = ''
task_id = ''
answers_str = []


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


def db_chapters():
    global chapters_str
    chapters_str = ''
    result = cursor.execute('SELECT name FROM Chapters')
    for elem in result:
        chapters_str += str(elem)[2:len(str(elem)) - 3] + ', '
    conn.commit()
    return chapters_str


def id_chapter(name_chapter: str):
    result = cursor.execute('SELECT id FROM Chapters WHERE name = ?', (name_chapter,))
    id_chapter = ''
    for elem in result:
        id_chapter += str(elem)[1:len(str(elem)) - 2]
    return int(id_chapter)


def db_sub_chapters(id_chapter: int):
    global sub_chapters_str
    sub_chapters_str = ''
    result = cursor.execute(
        'SELECT Subchapters.name FROM Subchapters INNER JOIN Chapters_Subchapters ON Subchapters.id = Chapters_Subchapters.id_Subchapters WHERE Chapters_Subchapters.id_Chapter = ?',
        (id_chapter,))
    for elem in result:
        sub_chapters_str += str(elem)[2:len(str(elem)) - 3] + ', '
    conn.commit()
    return sub_chapters_str


def id_sub_chapter(name_sub_chapter: str):
    result = cursor.execute('SELECT id FROM Subchapters WHERE name = ?', (name_sub_chapter,))
    id_sub_chapter = ''
    for elem in result:
        id_sub_chapter += str(elem)[1:len(str(elem)) - 2]
    return int(id_sub_chapter)


def db_levels():
    global level_str
    level_str = ''
    result = cursor.execute('SELECT name FROM levels')
    for elem in result:
        level_str += str(elem)[2:len(str(elem)) - 3] + ', '
    conn.commit()
    return level_str


def id_level(name_level: str):
    result = cursor.execute('SELECT id FROM levels WHERE name = ?', (name_level,))
    id_level = ''
    for elem in result:
        id_level += str(elem)[1:len(str(elem)) - 2]
    return int(id_level)


def db_tasks():
    global tasks_str
    tasks_str = ''
    result = cursor.execute(
        'SELECT tasks.number FROM tasks INNER JOIN result ON tasks.id = result.id WHERE result.Chapter = ? and result.Subchapter = ? and result.Level = ?',
        (chapter_id, sub_chapter_id, level_id))
    for elem in result:
        tasks_str += str(elem)[2:len(str(elem)) - 3] + ', '
    return tasks_str


def id_task(task_number):
    global task_id
    task_id = ''
    result = cursor.execute(
        'SELECT tasks.id FROM tasks INNER JOIN result ON tasks.id = result.id WHERE result.Chapter = ? and result.Subchapter = ? and result.Level = ? and tasks.number = ?',
        (chapter_id, sub_chapter_id, level_id, task_number))
    for elem in result:
        task_id += str(elem)[1:len(str(elem)) - 2]
    return task_id


def get_task_text(task_id):
    task_text = ''
    result = cursor.execute('SELECT name FROM tasks WHERE id = ?', (task_id,))
    for elem in result:
        task_text += str(elem)[2:len(str(elem)) - 3]
    return task_text


def get_answers():
    global answers_str
    answers_str = []
    result = cursor.execute('SELECT answer1, answer2, answer3, answer4 FROM tasks WHERE id = ?', (task_id,))
    for elem in result:
        for i in elem:
            answers_str.append(i)
    return answers_str


def right_answer():
    right_answer_str = ''
    result = cursor.execute('SELECT right_answer FROM tasks WHERE id = ?', (task_id,))
    for elem in result:
        right_answer_str += str(elem)[1:len(str(elem)) - 2]
    return str(right_answer_str)[1:len(right_answer_str) - 1]


@bot.message_handler(commands=['start'])
def start_message(message):
    db_chapters()
    db_levels()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Авторизоваться🔑")
    btn2 = types.KeyboardButton("Выбор раздела задачи🔎")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     'Привет! 👋 \nЯ бот-тренажер по физике, давай вместе порешаем задачи? \n \nЕсли ты еще не добавлен в систему, то напиши слово: "Привет"',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global chapter_id, sub_chapter_id, level_id
    '''
    if (message.text == "Авторизоваться🔑"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home)
        bot.send_message(message.chat.id, text="Как я могу помочь?", reply_markup=markup)
    '''

    if (message.text == "Выбор раздела задачи🔎"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in chapters_str.split(', '):
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home)
        bot.send_message(message.chat.id, text="Выбери раздел:", reply_markup=markup)

    elif (message.text in chapters_str):
        chapter_id = id_chapter(str(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in db_sub_chapters(id_chapter(str(message.text))).split(', '):
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home)
        bot.send_message(message.chat.id, text="Выбери подраздел:", reply_markup=markup)

    elif (message.text in sub_chapters_str):
        sub_chapter_id = id_sub_chapter(str(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in level_str.split(', '):
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home)
        bot.send_message(message.chat.id, text="Выбери уровень:", reply_markup=markup)

    elif (message.text in level_str):
        level_id = id_level(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in db_tasks().split(', '):
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home)
        bot.send_message(message.chat.id, text="Выбери номер задачи:", reply_markup=markup)

    elif (message.text in tasks_str):
        task_number = message.text
        bot.send_message(message.chat.id, text=get_task_text(id_task(task_number)))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in get_answers():
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        # btn_home = types.KeyboardButton('На главную🏡')
        # markup.add(btn_home)
        bot.send_message(message.chat.id, 'Выбери правильный ответ:', reply_markup=markup)

    elif (message.text in answers_str):
        if str(message.text) == str(right_answer()):
            bot.send_message(message.chat.id, 'Верно!✅')
        else:
            bot.send_message(message.chat.id, 'Неверно❌')

    elif (message.text == 'На главную🏡'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Авторизоваться🔑")
        btn2 = types.KeyboardButton("Выбор раздела задачи🔎")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         'Привет! 👋 \nЯ бот-тренажер по физике, давай вместе порешаем задачи? \n \nЕсли ты еще не добавлен в систему, то напиши слово: "Привет"',
                         reply_markup=markup)

    elif message.text == 'Авторизоваться🔑':
        bot.send_message(message.chat.id, 'Ты успешно авторизовался!')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'Авторизоваться🔑':
        bot.send_message(message.chat.id, 'Ты успешно авторизовался!')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


bot.polling(none_stop=True)
