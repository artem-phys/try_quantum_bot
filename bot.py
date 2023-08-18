import os
import telebot

from qiskit.visualization import plot_bloch_vector

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Я try_quantum_bot. С моей помощью можно познакомиться с миром квантовых вычислений")


@bot.message_handler(commands=['bloch_sphere'])
def bloch_sphere_handler(message):
    text = "Наберите в сообщении состояние для отображения на сфере Блоха"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, display_bloch_sphere_handler)


def display_bloch_sphere_handler(message):
    text = "Вот что получилось"

    result = plot_bloch_vector([0, 1, 0])

    result.savefig('bloch_state.png', dpi=300, bbox_inches="tight")
    bot.send_photo(message.chat.id, photo=open('bloch_state.png', 'rb'),
                   caption="Ваше состояние")


@bot.message_handler(func=lambda msg: True)
def dunno_all(message):
    dunno_text = "Я не знаю, как на это ответить"
    bot.reply_to(message, dunno_text)


bot.infinity_polling()
