from os import environ
from dotenv import load_dotenv
from googletrans import Translator

import re
import discord
import responses

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
translator = Translator()

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    token = environ["DISCORD_TOKEN"]

    # token = os.environ.get("DISCORD_TOKEN")
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Setting 'Playing ' status
        await client.change_presence(activity=discord.Game(name=f"Teamfight Tactics"))

    # bot response for user messages
    @client.event
    async def on_message(message):
        # if message.author == client.user:
        #     return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        # increment o7 counter
        if user_message[0] == 'o':
            try:
                f = open("counter.txt", "r")
                counter = int(f.readline())
                counterlen = len(str(counter)) + 1
            except:
                f = open("counter.txt", "a")
                f.write(str(0))
                counterlen = 0
            if user_message[1:counterlen] == str(counter):
                counter += 1
                f = open("counter.txt", "w")
                f.write(str(counter))

        # reply to "its time"
        if "its" in user_message or "it's" in user_message:
            # google translate for non-english languages
            language = await translator.detect(user_message)
            user_message = message.content.replace('\n', ' ')
            # confirm if language detected is really english
            if language.lang == 'en':
                for word in user_message.split(' '):
                    language = await translator.detect(word)
                    if language.lang != 'en':
                       break
            en_translated = await translator.translate(user_message, 'en', language.lang)
            # compare with regex
            language_re = "it(\')?s(\s)*time"
            if re.search(language_re, en_translated.text, re.IGNORECASE):
                message.content = "it's time"
                await send_message(message, message.content, is_private=False)

    client.run(token)
