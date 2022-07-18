import json
import os
from random import Random, random
import requests
import yake
import discord
from dotenv import load_dotenv

lmt = 1 ## Limit of gifs to be returned
devmode = False ## If true, bot will return a random gif 100% of the time
messagePercentInt=5 ## Percentage of messages to be checked for keywords


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENORAPIKEY')
ckey = os.getenv("ckey")


client = discord.Client() # Creates a client object

@client.event
async def on_message(message):
    firstchar = message.content[0]
    if firstchar == "&" and message.content[1:].strip() == "help":
        await message.channel.send("I'm a bot that sends gifs based on your message.\n")
        return

    # 5% chance of responding to a message
    if message.author == client.user: return
    if not devmode:
        if Random().randrange(0, 100) > messagePercentInt : return
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