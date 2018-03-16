import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(bot, update):
    update.effective_message.reply_text("Hi!")


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)

def errors(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (str(update), error))

def post_rules(bot, update):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    name = get_name(update)
    BOT_NAME = bot.username
    if update.message._new_chat_member.username == BOT_NAME:
        return False
    else:
        pprint('Room: '+str(chat_id))
        pprint('Chat_id: '+str(chat_id))

        logger.info("welcoming = "+name)
        msg = ("Welcome to "+ str(chat_id) % (name))

        message = bot.sendMessage(chat_id=user_id, text=msg)

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = str(os.getenv('BOT_TOKEN'))
    NAME = "desolate-hollows-39625"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, post_rules))
    dp.add_handler(CommandHandler('rules', post_rules))
    dp.add_error_handler(errors)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
