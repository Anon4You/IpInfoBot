import telebot
import requests
import time

with open('token.txt', 'r') as file:
    bot_token = file.read().strip()  

bot = telebot.TeleBot(bot_token)

debug_message = (
        "Your Ip-Info Bot Has started\n"
        "Contact https://t.me/alienkrishn\n"
        "To buy the advance verision of this bot"
                 )
print(debug_message) 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me an IP address to get its information.")

@bot.message_handler(func=lambda message: True)
def send_ip_info(message):
    ip_address = message.text.strip()

    loading_message = bot.reply_to(message, "Fetching information...")

    progress_length = 20 
    steps = 5 
    for i in range(steps + 1): 
        filled_length = int(progress_length * i // steps)
        unfilled_length = progress_length - filled_length
        progress = '▮' * filled_length + '▯' * unfilled_length

        bot.edit_message_text(f"Fetching information... [{progress}] {i * 20}% complete",
                              chat_id=loading_message.chat.id,
                              message_id=loading_message.message_id)
        time.sleep(1) 

    response = requests.get(f"http://ip-api.com/json/{ip_address}")

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            info = (
                f"🏠 *IP Address:* {data['query']}\n"
                f"🌍 *Country:* {data['country']}\n"
                f"🌆 *Region:* {data['regionName']}\n"
                f"🏙️ *City:* {data['city']}\n"
                f"✉️ *ZIP:* {data['zip']}\n"
                f"📍 *Latitude:* {data['lat']}\n"
                f"🌐 *Longitude:* {data['lon']}\n"
                f"📡 *ISP:* {data['isp']}\n"
                f"🏢 *Organization:* {data['org']}\n"
                f"🔗 *AS:* {data['as']}\n"
                f"🌍 *Google Map:* https://maps.google.com/maps?q={data['lat']},{data['lon']}\n\n"
                f"👤 *Created by:* [Alienkrishn](https://github.com/Alienkrishn)"
            )
        else:
            info = "Could not retrieve information for that IP address."
    else:
        info = "Error fetching data from the IP API."

    bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)

    bot.reply_to(message, info, parse_mode='Markdown')

if __name__ == '__main__':
    bot.polling()
