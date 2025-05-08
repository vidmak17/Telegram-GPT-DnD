import os
import telebot
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ти — майстер гри в DnD. Веди пригоду, описуй сцени, відповідай гравцям, кидай кубики за них або пропонуй варіанти дій. Відповідай українською."},
            {"role": "user", "content": user_text}
        ]
    )

    bot.reply_to(message, gpt_response.choices[0].message.content)

bot.infinity_polling()
