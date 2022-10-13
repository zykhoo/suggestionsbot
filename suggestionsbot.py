#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to compile suggestions.
"""





import logging
import json



from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(update, context):
    update.message.reply_text("""```/new_list listname``` to create a new list (please remove whitespace) \n 
```/del_list listname``` to delete an existing list \n
```/new_suggestion listname suggestion``` to add a suggestion to an existing list\n
```/del_suggestion listname suggestion``` to delete a suggestion from an existing list \n
```/show_suggestion listname``` to view all suggestions in an existing list\n
```/show_lists``` to show all lists""")

def new_list(update, context):
    command, content = update.message.text.split(" ", 1)
    dictionary = json.loads(open("suggestions.json","r").read())
    dictionary["%s" %content] = []
    json.dump(dictionary, open("suggestions.json","w"))
    update.message.reply_text('Created new list %s' %content)

def del_list(update, context):
    command, content = update.message.text.split(" ", 1)
    dictionary = json.loads(open("suggestions.json","r").read())
    del dictionary["%s" %content]
    json.dump(dictionary, open("suggestions.json","w"))
    update.message.reply_text('Deleted list %s' %content)

def new_suggestion(update, context):
    command, content = update.message.text.split(" ", 1)
    ls, suggestion = content.split(" ", 1)
    dictionary = json.loads(open("suggestions.json","r").read())
    dictionary["%s" %ls].append("%s" %suggestion)
    json.dump(dictionary, open("suggestions.json","w"))
    update.message.reply_text('Added suggestion %s to list %s' %(suggestion, ls))

def del_suggestion(update, context):
    command, content = update.message.text.split(" ", 1)
    ls, suggestion = content.split(" ", 1)
    dictionary = json.loads(open("suggestions.json","r").read())
    dictionary["%s" %ls].remove("%s" %suggestion)
    json.dump(dictionary, open("suggestions.json","w"))
    update.message.reply_text('Removed suggestion %s from list %s' %(suggestion, ls))

def show_suggestion(update, context):
    command, ls = update.message.text.split(" ", 1)
    dictionary = json.loads(open("suggestions.json","r").read())
    update.message.reply_text(dictionary["%s" %ls]) 

def show_lists(update, context):
    dictionary = json.loads(open("suggestions.json","r").read())
    update.message.reply_text(', '.join(str(key) for key, value in dictionary.items()))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("UPDATE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    data = {}

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new_list", new_list))
    dp.add_handler(CommandHandler("new_suggestion", new_suggestion))
    dp.add_handler(CommandHandler("del_list", del_list))
    dp.add_handler(CommandHandler("del_suggestion", del_suggestion))
    dp.add_handler(CommandHandler("show_suggestion", show_suggestion))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("show_lists", show_lists))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
