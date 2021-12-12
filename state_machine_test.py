import unittest
import telebot
from telebot import TeleBot
from transitions import Machine
from pythonProject.state_machine_1 import size, pay, confirmation1, confirmation2, confirmation3, confirmation4, \
    completion, batman, Pizza, dialog, list1


class State_machine(unittest.TestCase):
    def test_send_text_1(self):
        batman = Pizza()
        print(batman.state)
        dialog(batman, 'большую')
        self.assertEqual(batman.state, pay)


    def test_send_text_2(self):
        batman = Pizza()
        dialog(batman, 'большую')
        dialog(batman, 'картой')
        dialog(batman, 'да')
        self.assertEqual(batman.state, completion)


    def test_send_text_3(self):
        batman = Pizza()
        dialog(batman, 'маленькую')
        dialog(batman, 'наличкой')
        dialog(batman, 'да')
        self.assertEqual(batman.state, completion)


    def test_send_text_4(self):
        batman = Pizza()
        dialog(batman, [1, 2, 3])
        self.assertEqual(batman.state, size)


if __name__ == '__main__':
    unittest.main()
