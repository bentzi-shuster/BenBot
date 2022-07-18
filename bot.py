import json
import os
from random import Random, random
import requests
import yake
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENORAPIKEY')  # click to set to your apikey
lmt = 1
ckey = "discord_bot_key"  # click to set to your ckey


client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
@client.event
async def on_message(message):
    # 5% chance of responding to a message
    if message.author == client.user: return
    if Random().randrange(0, 100) > 5 : return
    async def reply(msg):
        kw_extractor = yake.KeywordExtractor()
        keywords = kw_extractor.extract_keywords(msg)
        longest_phrase = max(keywords, key=lambda x: len(x[0]))
        longest_phrase = longest_phrase[0]
        search_term = longest_phrase
        r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))
        if r.status_code == 200:
            top_gif = json.loads(r.content)
            messageURLGIF = top_gif['results'][0]['media_formats']
            messageURLGIF = messageURLGIF['gif']['url']
            await message.channel.send(messageURLGIF)
        else:
            top_gif = None
        return 

    await reply(message.content)
    
    

client.run(TOKEN)