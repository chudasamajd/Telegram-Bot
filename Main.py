from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode
from telegram.forcereply import ForceReply
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.callbackquery import CallbackQuery

from telegram.ext.callbackqueryhandler import CallbackQueryHandler
import requests
import wikipedia

headers = {'apikey': 'a84131c0-afda-11ea-bf97-157d5da8d462'}
bot = Bot("1104771102:AAHh30FHONe4lSCqk7LjDjLshA-VE98fDTg")

# getting the bot details
print(bot.get_me())

updater = Updater("1104771102:AAHh30FHONe4lSCqk7LjDjLshA-VE98fDTg",
                  use_context=True)

dispatcher: Dispatcher = updater.dispatcher

keyword = ''
chat_id = ''


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def bop(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
        parse_mode=ParseMode.HTML,
    )
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def show_keyboard(update: Update, context: CallbackContext):
    global keyword,chat_id
  

    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton("ABOUT", callback_data='ABOUT'),
        InlineKeyboardButton("IMAGE", callback_data='IMAGE')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update, context):
    global keyword,chat_id

    query: CallbackQuery = update.callback_query
    #query.answer()
    #query.edit_message_text(text="Loading...".format(query.data))
    if query.data == "ABOUT":

        summary = wikipedia.summary(keyword)

        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML,
        )
    if query.data == "IMAGE":
        params = (
            ("q", keyword),
            ("tbm", "isch"),
        )

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)

        data = response.json()
        url = data['image_results'][0]['thumbnail']


        bot.send_photo(chat_id=chat_id, photo=url)


updater.dispatcher.add_handler(MessageHandler(Filters.text, show_keyboard))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling()
