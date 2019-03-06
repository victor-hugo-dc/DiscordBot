import discord
from discord.ext import commands
import requests
import json
from bs4 import BeautifulSoup

TOKEN = '' #Insert Bot Token from Discord
COMMAND_PREFIX = ('!', '+', '.') #Command Prefixes can be a string or a tuple of strings
NICK = '' #Nickname
CB_USER = '' #Cleverbot.io user
CB_KEY = '' #Cleverbot.io key

client = commands.Bot(command_prefix = COMMAND_PREFIX)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='with Humans'))
    print('Bot is ready.')

@client.event
async def on_message(message):
    print('message recieved, sent')
    await client.process_commands(message)

@client.command()
async def weather():
    #Weather command to get forecast in Centreville, VA. 
    #Change coordinates for your city.
    COORD = {
        "x": 38.8404,
        "y": -77.4289
    }
    r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=COORD["x"], y=COORD["y"]))
    forecast = r.json()['properties']['periods'][0]['detailedForecast']
    await client.say(forecast)

@client.command()
async def ping():
    await client.say('Pong!')

@client.command(pass_context=True)
async def set(ctx):
    msg = ctx.message.content
    msg = msg[msg.find('set') + 3:]
    await client.change_presence(game=discord.Game(name=msg))

@client.command(pass_context=True)
async def echo(ctx):
    msg = ctx.message.content
    msg = msg[msg.find('echo') + 4:]
    await client.say(msg)

@client.command(pass_context=True)
async def chat(ctx):
    body = {'user': CB_USER,'key': CB_KEY,'nick': NICK}
    requests.post('https://cleverbot.io/1.0/create', data=body)
    msg = ctx.message.content
    msg = msg[msg.find('chat') + 4:]
    query = {'user': CB_USER,'key': CB_KEY,'nick': NICK, 'text': msg}
    r = requests.post('https://cleverbot.io/1.0/ask', data=query)
    r = json.loads(r.text)

    if r['status'] == 'success':
        await client.say(r['response'])
    else:
        await client.say('Error')

@client.command(pass_context=True)
async def youtube(ctx):
    msg = ctx.message.content
    msg = msg[msg.find('youtube') + 7:].replace(' ', '%20').lower()
    r = requests.get('https://www.youtube.com/results?search_query='+msg)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
            result = link.get('href')
            if result.startswith('/watch'):
                break
    await client.say('https://www.youtube.com'+result)

client.run(TOKEN)
