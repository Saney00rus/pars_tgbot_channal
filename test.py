from botset import token
import telebot

bot = telebot.TeleBot(token)
chat_id = '167749311'  # Канал
bot.send_message(chat_id, 'Бот запущен!')