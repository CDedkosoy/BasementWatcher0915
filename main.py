import logging
from typing import Final
import os
import json
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from responses import get_response

#   STEP 0: LOAD TOKEN FROM SOMEWHERE SAFE + SETUP LOG
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

logging.basicConfig(filename='log.txt',encoding='utf-8',level=logging.DEBUG)
logging.debug('DEBUG')
logging.info('INFO')
logging.warning('WARNING')
logging.error('ERROR')
logging.critical('CRITICAL')

#   STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

#   STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        log_message = '(Message was empty because intents were not enabled probably)'
        print(log_message)
        logging.info(log_message)
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        logging.warning(e)
#    get_message: str = send_message(text)
#    print(get_message)

#   STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    log_message = f'{client.user} is now running.'
    print(log_message)
    logging.debug(log_message)
    
#    user = await client.fetch_user(1015484539365232680)
#    user = await client.fetch_user(1168947089707905054)
#    user = await client.fetch_user(956320835214401536)
#    await user.send('Matching pfp pictures? What does he lose to you? XDD')

#   STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user :
        return
    
    if message.channel.type == discord.ChannelType.private:
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)
    
        log_message = f'[{channel}] {username}: "{user_message}"'
        print(log_message)
        logging.info(log_message)
        await send_message(message, user_message)
        
    elif client.user.mentioned_in(message):
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)
    
        log_message = f'[{channel}] {username}: "{user_message}"'
        print(log_message)
        logging.info(log_message)
        await send_message(message, user_message)

#   STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()