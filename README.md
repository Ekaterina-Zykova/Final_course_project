# Telegram-Repost-Bot
Telegram bot that accepts incoming messages and repost them on its own behalf to other telegram channels.
## Clone this repo
```shell
git clone https://github.com/enzkva/Final_course_project.git
```
## Edit
Edit variables in file config.py

    token = ''  # your bot token
    
    bot = ''  # your bot name
    
    channel = ''  # channel where your bot is an admin
    
    api_id = 0123  # api id of your Client API 
    
    api_hash = ''  # api hash of your Client API 
    
    session_str = ''  # string session of your Client API

## Installation
```shell
pip3 install -r requirements.txt
```
## Start bot
```shell
python bot.py
```
1. Add a bot in your channel.
2. Go to channel settings / users list / promote user to admin
3. Click SAVE button
4. Enjoy!
## Commands
### /start
Starts the initial dialog with the bot
### /help
Gets information about commands
### /add_channel
Adds channel in channel list
### /delete_channel
Deletes channel from channel list
### /channel_list
Shows channel list

## Shut down the bot
Press Ctrl-C