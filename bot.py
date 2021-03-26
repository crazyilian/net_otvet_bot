from telethon import TelegramClient
from telethon import events
from random import choice
import logging
import os


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
BOT_NAME = "@net_otvet_bot"


with open('net.txt', 'r', encoding='utf-8') as f:
    net = f.read().strip().split()
with open('da.txt', 'r', encoding='utf-8') as f:
    da = f.read().strip().split()


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)нет\W*$', incoming=True))
async def handle_net(event):
    word = choice(net).capitalize()
    await event.respond(word)


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)да\W*$', incoming=True))
async def handle_da(event):
    word = choice(da).capitalize()
    await event.respond(word)



@bot.on(events.NewMessage(pattern=r'(?i)^лол$', incoming=True))
async def handle_kek(event):
    await event.respond('Кек')
    await event.respond('Чебурек')
    


@bot.on(events.NewMessage(pattern=r'(?i)^кек$', incoming=True))
async def handle_lol(event):
    await event.respond('Лол')
    await event.respond('Арбидол')


@bot.on(events.NewMessage(pattern=fr'(?i)^/help({BOTNAME}|)(\s|$)', incoming=True))
async def help(event):
    await event.respond('''
Привет! 🖐
Без лишних слов, напиши:
▪️ Да
▪️ Нет
▪️ Кек
▪️ Лол
Наслаждайся остроумным общением с друзьями! 👌
    '''.strip())


bot.run_until_disconnected()
