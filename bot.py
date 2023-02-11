import telethon
import random
import logging
import os
import json
import asyncio
import time


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

bot = telethon.TelegramClient('bot', int(os.environ['API_ID']), os.environ['API_HASH']).start(bot_token=os.environ['BOT_TOKEN'])
BOTNAME = "@net_otvet_bot"
blocked_chats = dict()

with open('words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

da = {}
net = {}
for word in words:
    if word.endswith('да'):
        da[word] = words[word]
    else:
        net[word] = words[word]


async def unblock_chat(chatid, until):
    await asyncio.sleep(max(0, until - time.time()))
    if blocked_chats.get(chatid, 0) <= time.time():
        blocked_chats.pop(chatid)


def block_chat(chatid, timeout):
    until = time.time() + timeout
    blocked_chats[chatid] = until
    asyncio.get_running_loop().create_task(unblock_chat(chatid, until))


def choose(words):
    base = random.choice(list(words.keys()))
    prefix = random.choice(words[base])
    return (prefix + ' ' + base).strip().capitalize()


@bot.on(telethon.events.NewMessage(pattern=r'(?i)^(|.*\W)([nн]+[eе]+[tт]+)\W*$', incoming=True, func=lambda e: e.chat_id not in blocked_chats))
async def handle_net(event):
    word = choose(net)
    await event.reply(word)
    logging.info(f'{event.chat_id}   \tНет - {word}')
    if not isinstance(msg.chat, telethon.types.User):
        block_chat(event.chat_id, 3 * 60)


@bot.on(telethon.events.NewMessage(pattern=r'(?i)^(|.*\W)([dд]+[aа]+)\W*$', incoming=True, func=lambda e: e.chat_id not in blocked_chats))
async def handle_da(event):
    word = choose(da)
    await event.reply(word)
    logging.info(f'{event.chat_id}   \tДа - {word}')
    if not isinstance(msg.chat, telethon.types.User):
        block_chat(event.chat_id, 3 * 60)



@bot.on(telethon.events.NewMessage(pattern=fr'(?i)^/help({BOTNAME}|)(\s|$)', incoming=True))
async def help(event):
    await event.respond('''
Привет! 🖐
Смысл бота очень простой. Попробуй написать сообщение, оканчивающееся на:
▪️ Да
▪️ Нет
Добавь бота в группу и наслаждайся остроумным общением! 👌
(не забудьте предоставить права на чтение всех сообщений).

Бот не будет отвечать на сообщения в одном чате чаще, чем 1 раз в 3 минуты. В личных сообщениях он работает без ограничений.
    '''.strip())

@bot.on(telethon.events.NewMessage(pattern=fr'(?i)^/start({BOTNAME}|)(\s|$)', incoming=True))
async def start(event):
    await help(event)


bot.run_until_disconnected()
