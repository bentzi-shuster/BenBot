import json
from ntpath import join
import os
from random import Random, random
import requests
import yake
import discord
from dotenv import load_dotenv
import csv

lmt = 1 ## Limit of gifs to be returned
devmode = True ## If true, bot will return a random gif 100% of the time
messagePercentInt=10 ## Percentage of messages to be checked for keywords
csvpath='./data.csv' ## Path to csv file

def get_channel_filter():
    csvfile = open(csvpath, 'r')
    reader = csv.reader(csvfile)
    channelFilterRow = next(reader)
    channelFilter = channelFilterRow[1:]
    channelFilter = [x.strip().replace('\n', '') for x in channelFilter]
    csvfile.close()
    return channelFilter
def set_channel_filter(newFilter):
    csvfile = open(csvpath, 'r')
    reader = csv.reader(csvfile)
    channelFilterRow = next(reader)
    csvfile.close()
    csvfile = open(csvpath, 'w')
    writer = csv.writer(csvfile)
    channelFilterRow[1:] = newFilter
    writer.writerow(channelFilterRow)
    csvfile.close()



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
apikey = os.getenv('TENORAPIKEY')
ckey = os.getenv("ckey")


client = discord.Client() # Creates a client object

@client.event
async def on_message(message):
    channelFilter=get_channel_filter()
    firstchar = message.content[0]
    if firstchar == "&":
        command =message.content[1:].strip().lower()
        # if has admin rights
        if message.author.guild_permissions.administrator:
            if command == "addchannel":
                if message.channel.name in channelFilter:
                    await message.channel.send(message.channel.name + " already in filter")
                else:
                    channelFilter.append(message.channel.name)
                    set_channel_filter(channelFilter)
                    await message.channel.send(message.channel.name + " added to filter")
            
            elif command == "removechannel":
                if message.channel.name in channelFilter:
                    channelFilter.remove(message.channel.name)
                    set_channel_filter(channelFilter)
                    await message.channel.send("BenBot removed from " + message.channel.name)
                else:
                    await message.channel.send("BenBot is not in " + message.channel.name)
                return
            elif command == "clearfilter":
                channelFilter = []
                set_channel_filter(channelFilter)
                await message.channel.send("Filter cleared")
                return
        
        if command == "listchannels":
            await message.channel.send("BenBot is in the following channels: " + str(channelFilter))
            return
        elif command  == "help":
            await message.channel.send("""
I'm a bot that sends gifs based on your message.\n
To add a channel to the list of channels I will respond to, use the command &addchannel.\n
To remove a channel from the list of channels I will respond to, use the command &removechannel.\n
To see the list of channels I will respond to, use the command &listchannels.\n
To see the list of commands, use the command &help""")
            return


    # 5% chance of responding to a message
    if message.author == client.user: return
    for channel in get_channel_filter():
        if channel == message.channel.name:
            break
    else:
        return
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