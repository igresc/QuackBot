import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import asyncio
import time
import requests
from sound import joke_to_sound_file

client = discord.Client()
bot_token = "***REMOVED***" # Bot secret token https://discord.com/developers/applications

#           EscuadronPZON           GAMBLING
guild_ids=[265806519583506432, 494520437603172362]

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=False)

# icanhazdadjoke.com api definitions
dadjoke_url = "https://icanhazdadjoke.com/"
headers = {'Accept': 'application/json', 'User-Agent': 'Api tests (sergicastro2001@gmail.com)'}

@slash.slash(
    name="ping",
    description="Ping QuackBot",
    guild_ids=guild_ids
)
async def _ping(ctx:SlashContext):
    await ctx.send("Pong!")

@bot.event
async def on_ready():
    print("Bot is ready!")
    # print('We have logged in as {0.user}'.format(client))

@bot.command()
async def joke(ctx):
    r = requests.get(url=dadjoke_url, headers=headers)
    joke = r.json()
    await ctx.send("{}".format(joke["joke"]))
    return joke["joke"]

# @bot.command()
# async def ping(ctx):
#     user_id = ctx.message.author.id
#     await ctx.send("<@%s> Pong!" % user_id)

@bot.command()
async def banoflife(ctx):
    args = ctx.message.content.split(" ")
    if len(args) >= 2:
        await ctx.message.channel.send("{} asi do vaneado dela bida".format(args[1]))
        print(args)
    else:
        userID = ctx.message.author.id
        await ctx.message.channel.send("<@{}> asi do vaneado dela bida".format(userID), tts=True)
        print(userID)

@bot.command(name="joina")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    #await ctx.send("Joined the voice channel {}".format(ctx.author.voice.channel))

@bot.command(name="leavea")
async def leave(ctx):
    await ctx.voice_client.disconnect()

#@bot.command()
@slash.slash(
    name="joke_tts",
    description="Tells you a dad joke into your ear.",
    guild_ids=guild_ids
)
async def _joke_tts(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)

    if not voice_client:
        await join(ctx)
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    joke_text = await joke(ctx)
    joke_to_sound_file(joke_text)
    audio_source = discord.FFmpegPCMAudio('joke.mp3')

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)

# @client.event
# async def on_message(message):
#     userID = message.author.id
#     #if userID == 301430727008976908:
#     if userID == 257592218888568832:
#         await message.channel.send("<@%s> calla puto." % userID)
#         await message.delete()

#     # channel = message.channel
#     # print("Channel", channel)
#     print("UserID", userID)
#     print("Message", message.content)   

@bot.listen
async def on_message(message):
    print(message)
    
bot.run(bot_token)
client.run(bot_token)
