from telethon import TelegramClient
from telethon import events
from random import choice
import logging
import os


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
BOTNAME = "@net_otvet_bot"


with open('net.txt', 'r', encoding='utf-8') as f:
    net = f.read().strip().split()
with open('da.txt', 'r', encoding='utf-8') as f:
    da = f.read().strip().split()




@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)(не+т|ne+t)\W*$', incoming=True))
async def handle_net(event):
    word = choice(net).capitalize()
    await event.respond(word)
    print(event.chat_id, '  \tНет -', word)


@bot.on(events.NewMessage(pattern=r'(?i)^(|.*\s)(да+|da+)\W*$', incoming=True))
async def handle_da(event):
    word = choice(da).capitalize()
    await event.respond(word)
    print(event.chat_id, '  \tДа -', word)


@bot.on(events.NewMessage(pattern=r'(?i)^(ло+л|lo+l)$', incoming=True))
async def handle_kek(event):
    await event.respond('Кек')
    await event.respond('Чебурек')
    print(event.chat_id, '  \tЛол - Кек Чебурек')


@bot.on(events.NewMessage(pattern=r'(?i)^(ке+к|ke+k)$', incoming=True))
async def handle_lol(event):
    await event.respond('Лол')
    await event.respond('Арбидол')
    print(event.chat_id, '  \tКек - Лол Арбидол')


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
    '''.strip())




bot.run_until_disconnected()
