from telethon import TelegramClient
from telethon import events
from random import choice
import logging
import os
from datetime import datetime, timedelta


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
BOTNAME = "@net_otvet_bot"
block = dict()

with open('net.txt', 'r', encoding='utf-8') as f:
    net = f.read().strip().split()
with open('da.txt', 'r', encoding='utf-8') as f:
    da = f.read().strip().split()


def add_block(chatid):
    block[chatid] = datetime.now()


def is_in_block(chatid):
    if chatid not in block:
        return False
    dt = datetime.now() - block[chatid]
    return dt < timedelta(minutes=3)


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)(не+т|ne+t)\W*$', incoming=True, func=lambda e: not is_in_block(e.chat_id)))
async def handle_net(event):
    word = choice(net).capitalize()
    await event.respond(word)
    print(event.chat_id, '  \tНет -', word)
    add_block(event.chat_id)


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)(да+|da+)\W*$', incoming=True, func=lambda e: not is_in_block(e.chat_id)))
async def handle_da(event):
    word = choice(da).capitalize()
    await event.respond(word)
    print(event.chat_id, '  \tДа -', word)
    add_block(event.chat_id)


@bot.on(events.NewMessage(pattern=r'(?i)^(ло+л|lo+l)$', incoming=True, func=lambda e: not is_in_block(e.chat_id)))
async def handle_kek(event):
    await event.respond('Кек')
    await event.respond('Чебурек')
    print(event.chat_id, '  \tЛол - Кек Чебурек')
    add_block(event.chat_id)


@bot.on(events.NewMessage(pattern=r'(?i)^(ке+к|ke+k)$', incoming=True, func=lambda e: not is_in_block(e.chat_id)))
async def handle_lol(event):
    await event.respond('Лол')
    await event.respond('Арбидол')
    print(event.chat_id, '  \tКек - Лол Арбидол')
    add_block(event.chat_id)


@bot.on(events.NewMessage(pattern=fr'(?i)^/help({BOTNAME}|)(\s|$)', incoming=True))
async def help(event):
    await event.respond('''
Привет! 🖐
Без лишних слов, попробуй написать:
▪️ Да
▪️ Нет
▪️ Кек
▪️ Лол
Наслаждайся остроумным общением с друзьями! 👌

Таймаут ответов: 3 минуты.
    '''.strip())

@bot.on(events.NewMessage(pattern=fr'(?i)^/start({BOTNAME}|)(\s|$)', incoming=True))
async def start(event):
    await help(event)


bot.run_until_disconnected()
