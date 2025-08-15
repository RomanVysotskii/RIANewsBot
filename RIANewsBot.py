from bs4 import BeautifulSoup
import requests
import fake_useragent
import telebot
from telebot import types
import time
from requests import RequestException

#Создаём бота
token = "" #TODO: необходимо вставить токен тг-бота
bot = telebot.TeleBot(token)

#Парсим новости
def get_news(category_url, headers):
    try:
        response = requests.get(category_url)
        response.raise_for_status()
    except RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return []

    req = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(req.content, "lxml")

    news_blocks = soup.find_all("a", class_="list-item__title")

    news_list = []
    for block in news_blocks:
        title = block.get_text(strip=True)
        link = block["href"]
        news_list.append(f"{title}: {link}")

    return news_list

#Основная информация для парсинга
url = "https://ria.ru/"
headers = {
    "Accept": "*/*",
    "User-Agent": f"{fake_useragent.UserAgent}"
}

#Обработка команды "/start"
@bot.message_handler(commands=['start'])
def start(message):
    #Кнопки категорий
    markup = types.InlineKeyboardMarkup()
    politics = types.InlineKeyboardButton("Политика", callback_data="politics")
    inworld = types.InlineKeyboardButton('В мире', callback_data='inworld')
    economics = types.InlineKeyboardButton('Экономика', callback_data='economics')
    society = types.InlineKeyboardButton('Общество', callback_data='society')
    incidents = types.InlineKeyboardButton('Проишествия', callback_data='incidents')
    army = types.InlineKeyboardButton('Армия', callback_data='army')
    science = types.InlineKeyboardButton('Наука', callback_data='science')
    culture = types.InlineKeyboardButton('Культура', callback_data='culture')
    sport = types.InlineKeyboardButton('Спорт', callback_data='sport')
    tourism = types.InlineKeyboardButton('Туризм', callback_data='tourism')
    religion = types.InlineKeyboardButton('Религия', callback_data='religion')
    markup.row(politics)
    markup.row(inworld)
    markup.row(economics, society, incidents)
    markup.row(army, science, culture)
    markup.row(sport, tourism, religion)
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}! Выберите категорию, и мы отправим вам новости:", reply_markup=markup)

#Обработка выбора
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    news_list = []

    if call.data == "politics":
        news_list = get_news("https://ria.ru/politics/", headers)
    elif call.data == "inworld":
        news_list = get_news("https://ria.ru/world/", headers)
    elif call.data == "economics":
        news_list = get_news("https://ria.ru/economy/", headers)
    elif call.data == "society":
        news_list = get_news("https://ria.ru/society/", headers)
    elif call.data == "incidents":
        news_list = get_news("https://ria.ru/incidents/", headers)
    elif call.data == "army":
        news_list = get_news("https://ria.ru/defense_safety/", headers)
    elif call.data == "science":
        news_list = get_news("https://ria.ru/science/", headers)
    #Обработка подкатегорий "культуры"
    elif call.data == "culture":
        markup = types.InlineKeyboardMarkup()
        movie = types.InlineKeyboardButton("Кино и сериалы", callback_data="culture_movie")
        interview = types.InlineKeyboardButton("Интервью - культура", callback_data="culture_interview")
        theater = types.InlineKeyboardButton("Театр", callback_data="culture_theater")
        exhibitions = types.InlineKeyboardButton("Выставки", callback_data="culture_exhibitions")
        books = types.InlineKeyboardButton("Книги", callback_data="culture_books")
        show = types.InlineKeyboardButton("Шоубиз", callback_data="culture_show")
        lifestyle = types.InlineKeyboardButton("Стиль жизни", callback_data="culture_lifestyle")
        photo = types.InlineKeyboardButton("Фото - культура", callback_data="culture_photo")
        music = types.InlineKeyboardButton("Музыка", callback_data="culture_music")
        news_culture = types.InlineKeyboardButton("Новости культуры", callback_data="news_culture")
        ballet = types.InlineKeyboardButton("Балет", callback_data="culture_ballet")
        opera = types.InlineKeyboardButton("Опера", callback_data="culture_opera")
        back = types.InlineKeyboardButton("Назад", callback_data="back_to_main")
        markup.row(movie, interview)
        markup.row(theater, exhibitions, books)
        markup.row(show, lifestyle)
        markup.row(photo)
        markup.row(music, news_culture)
        markup.row(ballet, opera)
        markup.row(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите подкатегорию культуры:",
            reply_markup=markup
        )

        return
    #Обработка подкатегорий "спорта"
    elif call.data == "sport":
        markup = types.InlineKeyboardMarkup()
        football = types.InlineKeyboardButton("Футбол", callback_data="sport_football")
        hockey = types.InlineKeyboardButton("Хоккей", callback_data="sport_hockey")
        figure = types.InlineKeyboardButton("Фигурное катание", callback_data="sport_figure")
        tennis = types.InlineKeyboardButton("Теннис", callback_data="sport_tennis")
        fights = types.InlineKeyboardButton("Единоборства", callback_data="sport_fights")
        skiing = types.InlineKeyboardButton("Лыжные гонки", callback_data="sport_skiing")
        biathlon = types.InlineKeyboardButton("Биатлон", callback_data="sport_biathlon")
        formula1 = types.InlineKeyboardButton("Формула 1", callback_data="sport_formula1")
        zozh = types.InlineKeyboardButton("ЗОЖ", callback_data="sport_zozh")
        back = types.InlineKeyboardButton("Назад", callback_data="back_to_main")
        markup.row(football)
        markup.row(hockey, figure)
        markup.row(tennis, fights)
        markup.row(skiing, biathlon)
        markup.row(formula1, zozh)
        markup.row(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите подкатегорию спорта:",
            reply_markup=markup
        )

        return
    elif call.data == "tourism":
        news_list = get_news("https://ria.ru/tourism/", headers)
    elif call.data == "religion":
        news_list = get_news("https://ria.ru/religion/", headers)
    elif call.data == "culture_movie":
        news_list = get_news("https://ria.ru/category_kino/", headers)
    elif call.data == "culture_interview":
        news_list = get_news("https://ria.ru/category_intervyu---kultura/", headers)
    elif call.data == "culture_theater":
        news_list = get_news("https://ria.ru/category_teatr/", headers)
    elif call.data == "culture_exhibitions":
        news_list = get_news("https://ria.ru/tag_thematic_category_Vystavka/", headers)
    elif call.data == "culture_books":
        news_list = get_news("https://ria.ru/category_knigi/", headers)
    elif call.data == "culture_show":
        news_list = get_news("https://ria.ru/showbusiness/", headers)
    elif call.data == "culture_lifestyle":
        news_list = get_news("https://ria.ru/category_stil-zhizni/", headers)
    elif call.data == "culture_photo":
        news_list = get_news("https://ria.ru/category_foto---kultura/", headers)
    elif call.data == "culture_music":
        news_list = get_news("https://ria.ru/category_muzyka/", headers)
    elif call.data == "news_culture":
        news_list = get_news("https://ria.ru/category_novosti-kultury/", headers)
    elif call.data == "culture_ballet":
        news_list = get_news("https://ria.ru/category_balet/", headers)
    elif call.data == "culture_opera":
        news_list = get_news("https://ria.ru/category_opera/", headers)
    elif call.data == "sport_football":
        news_list = get_news("https://rsport.ria.ru/football/", headers)
    elif call.data == "sport_hockey":
        news_list = get_news("https://rsport.ria.ru/hockey/", headers)
    elif call.data == "sport_figure":
        news_list = get_news("https://rsport.ria.ru/figure_skating/", headers)
    elif call.data == "sport_tennis":
        news_list = get_news("https://rsport.ria.ru/tennis/", headers)
    elif call.data == "sport_fights":
        news_list = get_news("https://rsport.ria.ru/fights/", headers)
    elif call.data == "sport_skiing":
        news_list = get_news("https://rsport.ria.ru/lyzhnye-gonki/", headers)
    elif call.data == "sport_biathlon":
        news_list = get_news("https://rsport.ria.ru/biathlon/", headers)
    elif call.data == "sport_formula1":
        news_list = get_news("https://rsport.ria.ru/category_formula_1/", headers)
    elif call.data == "sport_zozh":
        news_list = get_news("https://rsport.ria.ru/zozh/", headers)
    elif call.data == "back_to_main":
        markup = types.InlineKeyboardMarkup()
        politics = types.InlineKeyboardButton("Политика", callback_data="politics")
        inworld = types.InlineKeyboardButton('В мире', callback_data='inworld')
        economics = types.InlineKeyboardButton('Экономика', callback_data='economics')
        society = types.InlineKeyboardButton('Общество', callback_data='society')
        incidents = types.InlineKeyboardButton('Проишествия', callback_data='incidents')
        army = types.InlineKeyboardButton('Армия', callback_data='army')
        science = types.InlineKeyboardButton('Наука', callback_data='science')
        culture = types.InlineKeyboardButton('Культура', callback_data='culture')
        sport = types.InlineKeyboardButton('Спорт', callback_data='sport')
        tourism = types.InlineKeyboardButton('Туризм', callback_data='tourism')
        religion = types.InlineKeyboardButton('Религия', callback_data='religion')
        test = types.InlineKeyboardButton("Test", callback_data="test")
        markup.row(politics)
        markup.row(inworld)
        markup.row(economics, society, incidents)
        markup.row(army, science, culture)
        markup.row(sport, tourism, religion)
        markup.row(test)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите категорию, и мы отправим вам новости:",
            reply_markup=markup
        )

        return

    else:
        news_list = []

    if not news_list:
        bot.send_message(call.message.chat.id, "Новости не найдены.")
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("Назад", callback_data="back_to_main")
        markup.add(back)
        bot.send_message(call.message.chat.id,"Если хотите вернуться, нажмите 'Назад'.", reply_markup=markup)
        return

    #Отправка новостей
    for news in news_list:
        bot.send_message(call.message.chat.id, news)
        time.sleep(2)

    #Кнопка "назад"
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("Назад", callback_data="back_to_main")
    markup.add(back)

    bot.send_message(call.message.chat.id,"Если хотите вернуться, нажмите 'Назад'.", reply_markup=markup)

try:
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    print(f"Произошла ошибка в Telegram API: {e}")