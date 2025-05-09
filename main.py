import os
import telebot
import openai
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    bot.process_new_updates([
        telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    ])
    return '', 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ти — майстер гри в DnD. Веди пригоду, описуй сцени, відповідай гравцям, кидай кубики. Відповідай українською."},
            {"role": "user", "content": user_text}
        ]
    )
    bot.reply_to(message, gpt_response.choices[0].message.content)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    app.run(host="0.0.0.0", port=10000)

