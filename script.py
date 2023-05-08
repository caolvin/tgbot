import logging
import random
import string

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the function to generate a random captcha
def generate_captcha(length=6):
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return captcha_text

# Define the function to handle the /start command
def start(update, context):
    # Generate and send a captcha to the user
    captcha_text = generate_captcha()
    keyboard = [[InlineKeyboardButton(captcha_text, callback_data=captcha_text)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Please enter the following captcha: {captcha_text}", reply_markup=reply_markup)

# Define the function to handle the callback from the captcha button
def button(update, context):
    query = update.callback_query
    query.answer()
    # Check if the user's input matches the captcha
    if query.data == query.message.text.split()[-1]:
        context.bot.send_message(chat_id=query.message.chat_id, text="You have passed the captcha. Welcome to the private group!")
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="Invalid captcha. Please try again.")

# Define the main function to start the bot
def main():
    # Set up the Telegram API access token
    token = '6150122964:AAFWTYnoth4NFyugEQfp1aqm46eaL2SUSUk'
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Define the handlers for the /start command and captcha button callback
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
