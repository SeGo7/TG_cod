import os
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
SUGGESTION_CHAT_ID = os.environ.get("SUGGESTION_CHAT_ID", "")

bot = telebot.TeleBot(TOKEN)

# ======================== Schedule ========================

WEEK_DAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
]

SCHEDULE_DATA = {
    "Понедельник": "1) Математика\n2) Физика\n3) Английский язык",
    "Вторник": "1) Информатика\n2) История\n3) Физкультура",
    "Среда": "1) Биология\n2) География\n3) Литература",
    "Четверг": "1) Химия\n2) Обществознание\n3) Английский язык",
    "Пятница": "1) Математика\n2) Физика\n3) ОБЖ",
    "Суббота": "Выходной",
}


def build_day_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for day in WEEK_DAYS:
        markup.add(day)
    return markup


@bot.message_handler(commands=["schedule"])
def handle_schedule(message: types.Message) -> None:
    msg = bot.send_message(
        message.chat.id, "Выберите день недели", reply_markup=build_day_keyboard()
    )
    bot.register_next_step_handler(msg, send_schedule)


def send_schedule(message: types.Message) -> None:
    day = message.text
    text = SCHEDULE_DATA.get(day, "Расписание не найдено")
    bot.send_message(message.chat.id, text)


# ======================== Cafeteria menu ========================
MENU_DATA = {
    "Понедельник": "Суп, каша, компот",
    "Вторник": "Борщ, котлеты, чай",
    "Среда": "Щи, плов, морс",
    "Четверг": "Гуляш, картофель, сок",
    "Пятница": "Рыбный день: уха, рис, компот",
    "Суббота": "Столовая закрыта",
}


@bot.message_handler(commands=["menu"])
def handle_menu(message: types.Message) -> None:
    msg = bot.send_message(
        message.chat.id, "Меню на какой день?", reply_markup=build_day_keyboard()
    )
    bot.register_next_step_handler(msg, send_menu)


def send_menu(message: types.Message) -> None:
    day = message.text
    text = MENU_DATA.get(day, "Меню не найдено")
    bot.send_message(message.chat.id, text)


# ======================== Student Council ========================
COUNCIL_TEXT = (
    "\U0001F451 Совет Министров:\n"
    "- Президент: Иван Иванов\n"
    "- Вице-президент: Мария Петрова\n"
    "- Министр культуры: Анна Смирнова"
)
COUNCIL_CHANNEL = "https://t.me/council_channel"
PRESIDENT_CONTACT = "https://t.me/president"


@bot.message_handler(commands=["council"])
def handle_council(message: types.Message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Связаться с президентом", url=PRESIDENT_CONTACT))
    markup.add(types.InlineKeyboardButton("Канал Совета", url=COUNCIL_CHANNEL))
    bot.send_message(message.chat.id, COUNCIL_TEXT, reply_markup=markup)


# ======================== Suggestions ========================
@bot.message_handler(commands=["suggest"])
def handle_suggest(message: types.Message) -> None:
    msg = bot.send_message(message.chat.id, "Напишите ваше предложение:")
    bot.register_next_step_handler(msg, forward_suggestion)


def forward_suggestion(message: types.Message) -> None:
    if SUGGESTION_CHAT_ID:
        bot.forward_message(SUGGESTION_CHAT_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Спасибо за ваше предложение!")


# ======================== Events ========================
EVENTS_TEXT = (
    "Ближайшие мероприятия:\n"
    "1) Олимпиада по математике - регистрация до 30 сентября.\n"
    "2) Волонтерский сбор макулатуры - 5 октября.\n"
    "3) Движение Первых - собрание каждую пятницу."
)


@bot.message_handler(commands=["events"])
def handle_events(message: types.Message) -> None:
    bot.send_message(message.chat.id, EVENTS_TEXT)


# ======================== Polls ========================
@bot.message_handler(commands=["poll"])
def handle_poll(message: types.Message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Да", callback_data="poll_yes"))
    markup.add(types.InlineKeyboardButton("Нет", callback_data="poll_no"))
    bot.send_message(message.chat.id, "Вам нравится наш бот?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("poll_"))
def handle_poll_vote(call: types.CallbackQuery) -> None:
    bot.answer_callback_query(call.id, "Голос учтен!")
    bot.send_message(call.message.chat.id, "Спасибо за участие в опросе!")


if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
