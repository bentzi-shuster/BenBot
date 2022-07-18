# BenBot
### This is a bot made by Ben to spam gifs 
##### the top of bot.py is has some config variables
```python
# bot.py config variables
lmt = 1 ## Limit of gifs to be returned
devmode = False ## If true, bot will return a random gif 100% of the time
messagePercentInt=5 ## Percentage of messages to be checked for keywords
```
##### a .env file is also required to run the bot 
```shell
DISCORD_TOKEN=
DISCORD_GUILD=
TENORAPIKEY=
ckey=
```
#### There is also a help command that can be accessed by typing `&help`, it just sends a message 

#### The bot uses the following libraries:
```python
# bot.py imports
import json
import os
from random import Random, random
import requests
import yake
import discord
from dotenv import load_dotenv
```
##### This bot is made by Ben, and comes as is with no warranty or support.