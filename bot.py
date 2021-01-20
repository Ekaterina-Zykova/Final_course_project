# -*- coding: utf-8 -*-

import logging

from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

import config
from db_users import add_channel, check_exist, delete_channel

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        f"Hello, {update.message.chat.first_name}! It's bot for reposts."
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        f"For add channel in channel list, write:\n    /add_channel @name"
        f"\nFor delete channel from channel list, write:\n    /delete_channel @name"
        f"\nFor show channel list, write:\n    /channel_list"
    )


def add_channel_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add_channel is issued."""
    if len(update.message.text.split()) == 1:
        answer = "For add channel in channel list, write:\n    /add_channel @name"
    else:
        channel = update.message.text.split()[1]
        answer = add_channel(user=update.message.from_user.id, channel=channel)
    update.message.reply_text(answer)


def delete_channel_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /delete_channel is issued."""
    if len(update.message.text.split()) == 1:
        answer = (
            "For delete channel from channel list, write:\n    /delete_channel @name"
        )
    else:
        channel = update.message.text.split()[1]
        answer = delete_channel(user=update.message.from_user.id, channel=channel)
    update.message.reply_text(answer)


def channel_list_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /channel_list is issued."""
    channel_list = check_exist(user=update.message.from_user.id)
    if channel_list:
        answer = ""
        for channel in channel_list:
            answer += channel + "\n"
    else:
        answer = "Channel list is empty 😔 \nFor add channel in channel list, write:\n    /add_channel @name"
    update.message.reply_text(answer)


def repost_messages(update: Update, context: CallbackContext):
    """Send messages to channels from the channel list when the message is sent to the bot"""
    channel_list = check_exist(user=update.message.from_user.id)
    if channel_list:
        for channel in channel_list:
            update.message.copy(chat_id=channel)
    else:
        update.message.reply_text(
            "Channel list is empty 😔 "
            "\nFor add channel in channel list, write:\n    /add_channel @name"
        )


def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=config.token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add_channel", add_channel_command))
    dispatcher.add_handler(CommandHandler("delete_channel", delete_channel_command))
    dispatcher.add_handler(CommandHandler("channel_list", channel_list_command))

    # on noncommand i.e message -  repost in channels
    dispatcher.add_handler(MessageHandler(Filters.update.message, repost_messages))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == "__main__":
    main()
