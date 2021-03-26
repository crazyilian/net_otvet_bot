from telethon import events
import logging
from random import choice
import os


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])


with open('net.txt', 'r', encoding='utf-8') as f:
    net = f.read().strip().split()
with open('da.txt', 'r', encoding='utf-8') as f:
    da = f.read().strip().split()


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)нет\W*$', incoming=True))
async def make(event):
    word = choice(net).capitalize()
    await event.respond(word)


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)да\W*$', incoming=True))
async def make(event):
    word = choice(da).capitalize()
    await event.respond(word)



@bot.on(events.NewMessage(pattern=r'(?i)^лол$', incoming=True))
async def make(event):
    await event.respond('Кек')
    await event.respond('Чебурек')
    


@bot.on(events.NewMessage(pattern=r'(?i)^кек$', incoming=True))
async def make(event):
    await event.respond('Лол')
    await event.respond('Арбидол')



bot.run_until_disconnected()
