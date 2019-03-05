import discord
from discord.ext import commands
import requests
import json

TOKEN = 'NTUxOTQzNTc4ODA1NjAwMjc3.D14VDg.Kx67OhzDhUAsyrAcof6vTBNwnds'
COMMAND_PREFIX = ('!', 'nav ', 'navrocko ')
NICK = 'NavRocko'
CB_USER = '6YMqiUa3FFVYA9oM'
CB_KEY = 'e2ojPdzkbbZXeO03QJmo8209qNqLcfhg'

client = commands.Bot(command_prefix = COMMAND_PREFIX)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='with bruvvas'))
    print('Bot is ready.')

@client.event
async def on_message(message):
    print('message recieved, sent')
    await client.process_commands(message)

@client.command()
async def weather():
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
    await client.say(ctx.message.content)

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
        await client.say('yo wtf')

@client.command()
async def extinguish():
    embed = discord.Embed(title = 'Navrocko@icloud.com',color=0x0080ff)
    embed.set_image(url='https://cdn.discordapp.com/attachments/141981735997931520/551473410996437036/image0.png')
    await client.say(embed=embed)

client.run(TOKEN)
