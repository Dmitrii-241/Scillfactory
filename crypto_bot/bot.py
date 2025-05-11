import telebot
from extensions import APIException, CurrencyConverter
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    text = ("📌 Формат запроса:\n<валюта1> <валюта2> <количество>\n"
            "Пример: доллар рубль 100\n\n"
            "Список команд:\n"
            "/values - доступные валюты")
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_currencies(message):
    text = "💰 Доступные валюты:\n- Евро (EUR)\n- Доллар (USD)\n- Рубль (RUB)"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.lower().split()
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(message, f"🔔 {amount} {base} = {result} {quote}")
    except APIException as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")
    except Exception:
        bot.reply_to(message, "❌ Неверный формат запроса")

if __name__ == "__main__":
    bot.polling()
