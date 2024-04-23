import sqlite3
import telebot
from telebot import types
import config
import gtts

bot = telebot.TeleBot("6915498321:AAEG09W9StyUxgOqV7-wNw73RocE7I46msQ")

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
task_number = ''
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
        id_sub_chapter = list(elem)[0]
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


def user():
    users = ''
    result = cursor.execute('SELECT username FROM users')
    for elem in result:
        users += str(elem)[2:len(str(elem)) - 3]
    return users


def get_image():
    image_str = ''
    result = cursor.execute('SELECT image FROM tasks WHERE id = ?', (task_id,))
    for elem in result:
        image_str = str(elem)[1:len(str(elem)) - 2]
    image_str = image_str[1: len(image_str) - 1]
    return image_str


def insert_estimation(success, user):
    attempt = 1
    result = cursor.execute('SELECT estimation FROM Estimations WHERE user = ? and task = ?', (user, task_id))
    for elem in result:
        attempt += 1
    estimation = 0
    if success:
        if level_id == 1:
            if attempt == 1:
                estimation = 3
            elif attempt == 2:
                estimation = 1
            else:
                estimation = 0
        elif level_id == 2:
            if attempt == 1:
                estimation = 5
            elif attempt == 2:
                estimation = 3
            elif attempt == 3:
                estimation = 1
            else:
                estimation = 0
        elif level_id == 3:
            if attempt == 1:
                estimation = 7
            elif attempt == 2:
                estimation = 5
            elif attempt == 3:
                estimation = 3
            else:
                estimation = 0
        elif level_id == 4:
            if attempt == 1:
                estimation = 10
            elif attempt == 2:
                estimation = 7
            elif attempt == 3:
                estimation = 5
            else:
                estimation = 0
    else:
        estimation = 0
    cursor.execute(
        'INSERT INTO Estimations (user, chapter, subchapter, level, task, estimation) VALUES (?, ?, ?, ?, ?, ?)',
        (user, chapter_id, sub_chapter_id, level_id, task_id, estimation))
    conn.commit()


def get_attempt(user):
    count = 0
    result = cursor.execute('SELECT estimation FROM Estimations WHERE user = ?', (user,))
    for elem in result:
        count += 1
    return count


def get_scores(user):
    scor = 0
    result = cursor.execute('SELECT estimation FROM Estimations WHERE user = ?', (user,))
    for elem in result:
        scor += int(list(elem)[0])
    return scor


@bot.message_handler(commands=['start'])
def start_message(message):
    db_chapters()
    db_levels()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Авторизоваться🔑")
    btn2 = types.KeyboardButton("Выбор раздела задачи🔎")
    btn3 = types.KeyboardButton("Статистика📊")
    markup.add(btn2, btn3)
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     'Привет! 👋 \nЯ бот-тренажер по физике, давай вместе порешаем задачи?',
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
        db_chapters()
        db_levels()
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
        global task_number
        task_number = message.text
        bot.send_message(message.chat.id, text=get_task_text(id_task(task_number)))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in get_answers():
            btn = types.KeyboardButton(elem)
            markup.add(btn)
        btn_audio = types.KeyboardButton('Озвучить🎵')
        btn_home = types.KeyboardButton('На главную🏡')
        markup.add(btn_home, btn_audio)
        if get_image() != 'on' and get_image() != '':
            bot.send_photo(message.chat.id, open(rf'images/{get_image()}', 'rb'))
        bot.send_message(message.chat.id, 'Выбери правильный ответ:', reply_markup=markup)

    elif (message.text in answers_str):
        if str(message.text) == str(right_answer()):
            bot.send_message(message.chat.id, 'Верно!✅')
            insert_estimation(True, message.from_user.id)
        else:
            bot.send_message(message.chat.id, 'Неверно❌')
            insert_estimation(False, message.from_user.id)

    elif (message.text == 'Озвучить🎵'):
        t1 = gtts.gTTS(get_task_text(id_task(task_number)), lang='ru')
        t1.save('Task.mp3')
        audio = open(r'Task.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()

    elif (message.text == 'Статистика📊'):
        bot.send_message(message.chat.id,
                         f'Твоя статистика📈:\n\nКоличетсво всех попыток при решении задач: {get_attempt(message.from_user.id)}🤩\n'
                         f'Количетсво баллов: {get_scores(message.from_user.id)}💪')

    elif (message.text == 'На главную🏡'):
        db_chapters()
        db_levels()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Выбор раздела задачи🔎")
        btn3 = types.KeyboardButton("Статистика📊")
        markup.add(btn2, btn3)
        bot.send_message(message.chat.id,
                         'Привет! 👋 \nЯ бот-тренажер по физике, давай вместе порешаем задачи?',
                         reply_markup=markup)

    elif message.text == 'Авторизоваться🔑':
        if str(message.from_user.username) not in user():
            bot.send_message(message.chat.id, 'Ты успешно авторизовался!🎉')

            us_id = message.from_user.id
            us_name = message.from_user.first_name
            us_sname = message.from_user.last_name
            username = message.from_user.username

            db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
        else:
            bot.send_message(message.chat.id, 'Ты уже авторизовался!')


bot.polling(none_stop=True)
