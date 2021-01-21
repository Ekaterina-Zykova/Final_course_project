import os

from pytest import mark
from telethon import TelegramClient

import config

pytestmark = mark.asyncio


async def test_start_command(client: TelegramClient):
    # Create a conversation
    async with client.conversation(config.bot) as conv:
        # Send a command
        await conv.send_message("/start")
        # Get response
        resp = await conv.get_response()
        # Make assertions
        assert "Hello! It's bot for reposts." in resp.raw_text


async def test_help_command(client: TelegramClient):
    async with client.conversation(config.bot) as conv:
        await conv.send_message("/help")
        resp = await conv.get_response()
        assert (
            f"For add channel in channel list, write:\n    /add_channel @name"
            f"\nFor delete channel from channel list, write:\n    /delete_channel @name"
            f"\nFor show channel list, write:\n    /channel_list" in resp.raw_text
        )


async def test_add_channel_command(client: TelegramClient):
    async with client.conversation(config.bot) as conv:
        await conv.send_message("/add_channel")
        resp1 = await conv.get_response()
        assert (
            "For add channel in channel list, write:\n    /add_channel @name"
            in resp1.raw_text
        )

        await conv.send_message("/add_channel @channel1")
        resp2 = await conv.get_response()
        assert "Done! You can write next name of channel." in resp2.raw_text

        await conv.send_message("/add_channel @channel1")
        resp3 = await conv.get_response()
        assert "The channel already exists in channel list." in resp3.raw_text


async def test_delete_channel_command(client: TelegramClient):
    async with client.conversation(config.bot) as conv:
        await conv.send_message("/delete_channel")
        resp1 = await conv.get_response()
        assert (
            "For delete channel from channel list, write:\n    /delete_channel @name"
            in resp1.raw_text
        )

        await conv.send_message("/delete_channel @channel1")
        resp2 = await conv.get_response()
        assert (
            "Channel is deleted from channel list!\nYou can write next name of channel."
            in resp2.raw_text
        )

        await conv.send_message("/delete_channel @channel1")
        resp3 = await conv.get_response()
        assert "The channel does not exist in channel list." in resp3.raw_text


async def test_channel_list_command(client: TelegramClient):
    async with client.conversation(config.bot) as conv:
        await conv.send_message("/channel_list")
        resp1 = await conv.get_response()
        assert (
            "Channel list is empty 😔 \nFor add channel in channel list, write:\n    /add_channel @name"
            in resp1.raw_text
        )

        await conv.send_message("/add_channel @channel1")
        await conv.get_response()
        await conv.send_message("/add_channel @channel2")
        await conv.get_response()
        await conv.send_message("/channel_list")
        resp2 = await conv.get_response()
        assert "@channel1\n@channel2" in resp2.raw_text


async def test_repost_messages_photo(client: TelegramClient):
    async with client as client:
        conv = client.conversation(config.bot)
        file_path = os.path.abspath("cat.jpeg")
        await conv.send_message("It's cat", file=file_path)
        messages = await client.get_messages(config.channel)
        assert "It's cat" in messages[0].message
        assert messages[0].media.photo.id != 0
