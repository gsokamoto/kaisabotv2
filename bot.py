from os import environ
from dotenv import load_dotenv

import discord
import responses

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    token = environ["TOKEN"]
    # bot.run(token)

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

        # if user_message[0] == '?':
        #     user_message = user_message[1:]
        #     await send_message(message, user_message, is_private=True)
        # else:
        # if '!' in user_message:
        if ("its" in user_message or "it's" in user_message) and ("time" in user_message):
            await send_message(message, user_message, is_private=False)

    # adding reaction roles
    # @client.event
    # async def on_raw_reaction_add(payload):
    #     message_id = payload.message_id
    #     if message_id == 1168615835837935637:
    #         guild_id = payload.guild_id
    #         guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    #
    #         if payload.emoji.name == 'inhouse':
    #             role = discord.utils.get(guild.roles, name='in-house')
    #         else:
    #             role = discord.utils.get(guild.roles, name=payload.emoji.name)
    #
    #         if role is not None:
    #             member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #             if member is not None:
    #                 await member.add_roles(role)

    # removing reaction roles
    # @client.event
    # async def on_raw_reaction_remove(payload):
    #     message_id = payload.message_id
    #     if message_id == 1168615835837935637:
    #         guild_id = payload.guild_id
    #         guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    #
    #         if payload.emoji.name == 'inhouse':
    #             role = discord.utils.get(guild.roles, name='in-house')
    #         else:
    #             role = discord.utils.get(guild.roles, name=payload.emoji.name)
    #
    #         if role is not None:
    #             member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #             if member is not None:
    #                 await member.remove_roles(role)


    client.run(token)
