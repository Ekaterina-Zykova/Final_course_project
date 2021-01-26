import asyncio

import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession

import config


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for all test cases."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client(event_loop) -> TelegramClient:
    client = TelegramClient(
        StringSession(config.session_str),
        config.api_id,
        config.api_hash,
        sequential_updates=True,
    )
    # Connect to the server
    await client.connect()
    # Issue a high level command to start receiving message
    await client.get_me()
    # Fill the entity cache
    await client.get_dialogs()

    yield client

    await client.disconnect()
    await client.disconnected
