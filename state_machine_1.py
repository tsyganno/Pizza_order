import app as app
import telebot
from telebot import TeleBot
from transitions import Machine
import os


TOKEN = os.environ.get('TOKEN')


bot: TeleBot = telebot.TeleBot(TOKEN, parse_mode=None)

size = 'Какую вы хотите пиццу? Большую или маленькую?'
pay = 'Как вы будете платить?'
confirmation1 = 'Вы хотите большую пиццу, оплата - наличкой?'
confirmation2 = 'Вы хотите маленькую пиццу, оплата - наличкой?'
confirmation3 = 'Вы хотите большую пиццу, оплата - картой?'
confirmation4 = 'Вы хотите маленькую пиццу, оплата - картой?'
completion = 'Спасибо за заказ'


class Pizza(object):
    states = [pay, size, confirmation1, confirmation2, confirmation3, confirmation4, completion]

    def __init__(self):

        self.machine = Machine(model=self, states=Pizza.states, initial=size)

        self.machine.add_transition('size_pizza', size, pay)

        self.machine.add_transition('cash_larg_pizza', pay, confirmation1)

        self.machine.add_transition('cash_small_pizza', pay, confirmation2)

        self.machine.add_transition('card_larg_pizza', pay, confirmation3)

        self.machine.add_transition('card_small_pizza', pay, confirmation4)

        self.machine.add_transition('yes', confirmation1, completion)

        self.machine.add_transition('yes', confirmation2, completion)

        self.machine.add_transition('yes', confirmation3, completion)

        self.machine.add_transition('yes', confirmation4, completion)

        self.machine.add_transition('start', '*', size)


batman = Pizza()
list1 = []
an_exception = ''


def dialog(batman, text):
    global list1
    global an_exception
    if batman.state == size and text == 'большую':
        batman.size_pizza()
        list1.append(text)
    elif batman.state == size and text == 'маленькую':
        batman.size_pizza()
        list1.append(text)
    elif text == 'наличкой' and batman.state == pay and 'большую' in list1:
        batman.cash_larg_pizza()
        list1 = []
    elif text == 'наличкой' and batman.state == pay and 'маленькую' in list1:
        batman.cash_small_pizza()
        list1 = []
    elif text == 'картой' and batman.state == pay and 'большую' in list1:
        batman.card_larg_pizza()
        list1 = []
    elif text == 'картой' and batman.state == pay and 'маленькую' in list1:
        batman.card_small_pizza()
        list1 = []
    elif text == 'да' and batman.state == confirmation1:
        batman.yes()
    elif text == 'да' and batman.state == confirmation2:
        batman.yes()
    elif text == 'да' and batman.state == confirmation3:
        batman.yes()
    elif text == 'да' and batman.state == confirmation4:
        batman.yes()
    else:
        an_exception = 'Прошу повторить'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, batman.state)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global an_exception
    human_message = message.text.lower()
    dialog(batman, human_message)
    if not an_exception:
        bot.send_message(message.from_user.id, batman.state)
        if batman.state == 'Спасибо за заказ':
            batman.start()
    else:
        bot.send_message(message.from_user.id, an_exception)
        an_exception = ''


bot.polling()
