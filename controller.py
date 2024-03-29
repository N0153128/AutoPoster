from newbot import Bot
import time
import asyncio
from get_and_store import GetAndStoreAndMore


# initializing objects
bot = Bot()
quote = GetAndStoreAndMore()

# initializing variables
upd = bot.link + '/getUpdates'
queue = asyncio.Queue()
localtime = time.asctime(time.localtime(time.time()))
launchtime = time.time()

# printing startup message
print(f'Started @ {localtime}')
print('Activated...')


# defining the function that would look up for updates and put it in a queue. every message that bot receives gets
# logged. when this function receives a message - it checks for spamming. if spam returns true - it will start up a
# process that would handle the message.
async def putin(q):
    while True:
        try:
            data = await bot.get_all()
            offset = bot.get_id(data) + 1
            await q.put(data)
            await bot.session.get(bot.link + '/getUpdates?offset=' + str(offset))
            await putout(queue)
        except (IndexError, KeyError, TypeError):
            pass


async def gen(data):
    d = await data.get()
    yield d


# this function is the message handler. every command is hardcoded for both private and group chats
async def putout(q):
    async for item in gen(q):
        try:
            if bot.get_message(item) == '/void':
                await bot.send_message(item, quote.get_random_quote(), get_chat=True, )
            elif bot.get_message(item) == '/void@nUnionVoid_bot':
                await bot.send_message(item, 'Void', get_chat=True)
            elif bot.get_message(item) == '/manual_post':
                await bot.send_message(item, chat_id='@known_quotes', message=quote.get_random_quote())
            elif bot.get_message(item) == '/get_amount':
                await bot.send_message(item, message=f'Total amount of quotes: {len(quote.list_quotes())}')
            elif bot.get_message(item) == '/add_ten':
                await bot.send_message(item, 'Launching parser...')
                quote.add_ten()
                await bot.send_message(item, 'Successfully added 10 new quotes')
            elif bot.get_message(item) == '/add_hundred':
                await bot.send_message(item, 'Launching parser...')
                quote.add_hundred()
                await bot.send_message(item, 'Successfully added 100 new quotes')
            elif bot.get_message(item) == '/add_thousand':
                await bot.send_message(item, 'Launching parser...')
                quote.add_thosand()
                await bot.send_message(item, 'Successfully added 1000 new quotes')
            elif bot.get_message(item) == '/add_10000':
                await bot.send_message(item, 'Launching parser...')
                quote.add_ten_thousand()
                await bot.send_message(item, 'Successfully added 10000 new quotes')
            elif bot.get_message(item) == '/add_100000':
                await bot.send_message(item, 'Launching parser...')
                quote.add_100000()
                await bot.send_message(item, 'Successfully added 100000 new quotes')
            elif bot.get_message(item) == '/begin_push':
                await quote.begin_push(item)
                pass
            elif bot.get_message(item)[:5] == '/addp':
                quote.add_lots(int(bot.get_message(item)[5:]))
                await bot.send_message(item, f'successfully added {bot.get_message(item)[5:]} of quotes')
            elif bot.get_message(item) == '/uptime':
                await bot.get_uptime(launchtime)
            elif not bot.get_message(item):
                pass

        except Exception as e:
            print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(putin(queue))
