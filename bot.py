import os
import telebot

from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_bloch_vector, plot_histogram

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я try_quantum_bot. С моей помощью можно познакомиться с миром квантовых вычислений")


# Отображение состояния на сфере Блоха
@bot.message_handler(commands=['bloch_sphere'])
def bloch_sphere_handler(message):
    text = "Набери в сообщении состояние для отображения на сфере Блоха"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, display_bloch_sphere_handler)


def display_bloch_sphere_handler(message):
    text = "Вот что получилось"

    result = plot_bloch_vector([0, 1, 0])

    result.savefig('bloch_state.png', dpi=300, bbox_inches="tight")
    bot.send_photo(message.chat.id, photo=open('bloch_state.png', 'rb'),
                   caption="Сфера Блоха")


# Отображение квантовой цепочки из QASM сода
    @bot.message_handler(commands=['qasm_code'])
    def qasm_handler(message):
        text = "Введи код на QASM, и я покажу твою цепочку"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, qasm_code_handler)

    def qasm_code_handler(message):
        text = "Вот что получилось"

        # Build a quantum circuit
        circuit = QuantumCircuit(3, 3)

        circuit.x(1)
        circuit.h(range(3))
        circuit.cx(0, 1)
        circuit.measure(range(3), range(3))

        qc_fig = circuit.draw('mpl')

        qc_fig.savefig('qc.png', dpi=300, bbox_inches="tight")
        sent_msg = bot.send_photo(message.chat.id, photo=open('qc.png', 'rb'),
                       caption="Квантовая цепочка")
        bot.register_next_step_handler(sent_msg, run_qc_handler)

    def run_qc_handler(message):
        text = "Вот что получилось"

        # Build a quantum circuit
        qc = QuantumCircuit(3, 3)

        backend = Aer.get_backend('statevector_simulator')
        job = backend.run(qc)
        counts = job.result().get_counts()

        counts_fig = circuit.draw('mpl')

        counts_fig.savefig('counts.png', dpi=300, bbox_inches="tight")
        sent_msg = bot.send_photo(message.chat.id, photo=open('counts.png', 'rb'),
                       caption="Результат запуска")


@bot.message_handler(func=lambda msg: True)
def dunno_all(message):
    dunno_text = "Я не знаю, как на это ответить"
    bot.reply_to(message, dunno_text)


bot.infinity_polling()
