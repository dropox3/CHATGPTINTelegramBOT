import logging
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

OPENAI_API_KEY = "YOUR API HERE"
TELEGRAM_BOT_TOKEN = "YOUR API HERE"

openai.api_key = OPENAI_API_KEY

def text_filter(update: Update) -> bool:
    return update.message and update.message.text and not update.message.text.startswith('/')

class GPTBot:
    def __init__(self):
        self.updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
        self._register_handlers()

    def _register_handlers(self):
        self.updater.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.dispatcher.add_handler(MessageHandler(text_filter, self.handle_message))

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Olá! Sou um bot com GPT. Envie-me uma mensagem e eu responderei.')

    def get_gpt_response(self, prompt):
        completion = openai.Completion.create(
            engine="davinci-codex",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        response = completion.choices[0].text
        return response

    def handle_message(self, update: Update, context: CallbackContext) -> None:
        input_prompt = update.message.text
        response = self.get_gpt_response(input_prompt)
        update.message.reply_text(response)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = GPTBot()
    bot.run()
