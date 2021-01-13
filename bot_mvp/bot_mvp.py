# -*- coding: utf-8 -*-

import config
import telebot
from db_users import add_channel, delete_channel, sql_query

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start", "help"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        f"Hello, {message.chat.first_name}! It's bot for reposts."
        f"\nFor add channel in repost list, write:\n    /add_channel @name"
        f"\nFor delete channel from repost list, write:\n    /delete_channel @name"
        f"\nFor show channels from reposts list write command:\n    /show_repost_list",
    )


@bot.message_handler(commands=["add_channel"])
def add_channel_command(message):
    if len(message.text.split()) == 0:
        bot.send_message(
            message.chat.id,
            "For add channel in repost list, write:\n    /add_channel @name",
        )
    else:
        channel = message.text.split()[1]
        ret = add_channel(message.from_user.id, channel)
        bot.send_message(message.chat.id, ret)


@bot.message_handler(commands=["delete_channel"])
def delete_channel_command(message):
    if len(message.text.split()) == 0:
        bot.send_message(
            message.chat.id,
            "For delete channel from repost list, write:\n    /delete_channel @name",
        )
    else:
        channel = message.text.split()[1]
        result = delete_channel(message.from_user.id, channel)
        bot.send_message(message.chat.id, result)


@bot.message_handler(commands=["show_repost_list"])
def show_repost_list_command(message):
    result = ""
    repost_list = sql_query(
        f"SELECT channel FROM users WHERE user_id={message.from_user.id}"
    )
    for channel in repost_list:
        result += channel[0] + "\n"
    bot.send_message(message.chat.id, result)


@bot.message_handler(content_types=["text", "photo"])
def repost_messages(message):
    repost_list = sql_query(
        f"SELECT channel FROM users WHERE user_id={message.from_user.id}"
    )
    if repost_list:
        if message.photo:
            temp_message = bot.send_photo(
                message.chat.id,
                message.photo[0].file_id,
                message.caption,
                disable_notification=True,
            )
        else:
            temp_message = bot.send_message(
                message.chat.id, message.text, disable_notification=True
            )
        if temp_message:
            for channel in repost_list:
                bot.forward_message(channel, message.chat.id, temp_message.message_id)
            bot.delete_message(temp_message.chat.id, temp_message.message_id)
    else:
        bot.send_message(
            message.chat.id,
            "Repost list is empty 😔 "
            "\nFor add channel in repost list, write:\n    /add_channel @name",
        )


bot.infinity_polling()
