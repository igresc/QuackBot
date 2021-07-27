from asyncio.tasks import sleep
import discord
from discord import voice_client
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import requests
from sound import string_to_sound_file
import os

# client = discord.Client()
bot_token = os.environ["BOT_TOKEN"] # Bot secret token https://discord.com/developers/applications

##### Guild server Ids #####
#            EscuadronPZON           GAMBLING
guild_ids=[265806519583506432, 494520437603172362]

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=False)

# icanhazdadjoke.com api definitions
dadjoke_url = "https://icanhazdadjoke.com/"
headers = {'Accept': 'application/json', 'User-Agent': 'Api tests (sergicastro2001@gmail.com)'}

##### Event on_ready() to know when the bot is ready and functional #####
@bot.event
async def on_ready():
    print("Bot is ready!")
    # print('We have logged in as {0.user}'.format(client))


##### Ping #####
@slash.slash(
    name="ping",
    description="Ping QuackBot",
    guild_ids=guild_ids
)
async def _ping(ctx:SlashContext):
    await ctx.send("Pong!")

##### Joke Text #####
# @slash.slash(
#     name="joke",
#     description="Tells a dad joke.",
#     guild_ids=guild_ids
# )
@bot.command(name="joke")
async def _joke(ctx):
    r = requests.get(url=dadjoke_url, headers=headers)
    joke = r.json()
    await ctx.send("{}".format(joke["joke"]))
    return joke["joke"]

##### Ban of life #####
@slash.slash(
    name="banoflife",
    description="Ban someone of life in a perfect grammar.",
    # options=[
    #            create_option(
    #              name="User",
    #              description="User to ban of life",
    #              option_type=3,
    #              required=False
    #            )
    #          ],
    guild_ids=guild_ids
)
async def banoflife(ctx):
    args = ctx.message.content.split(" ")
    if len(args) >= 2:
        await ctx.message.channel.send("{} asi do vaneado dela bida".format(args[1]))
        print(args)
    else:
        userID = ctx.message.author.id
        await ctx.message.channel.send("<@{}> asi do vaneado dela bida".format(userID), tts=True)
        print(userID)

##### Join authors voice Channel #####
@bot.command(name="joina")
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        try:
            vc = await channel.connect()
            source = discord.FFmpegPCMAudio("data/quack.mp3")
            vc.play(source)
        except discord.errors.ClientException:
            print("Bot already connected to a voice channel.")
    except AttributeError:
        await ctx.send("<@{}> You need to be in a voice channel".format(ctx.author.id))
    
    #await ctx.send("Joined the voice channel {}".format(ctx.author.voice.channel))

@bot.command(name="leavea")
async def leave(ctx):
    await ctx.voice_client.disconnect()

def rm_joke(filename):
    try:
        os.remove(filename)
    except PermissionError as e:
        print(e)

##### Joke TTS #####
@slash.slash(
    name="joke_tts",
    description="Tells you a dad joke into your ear.",
    guild_ids=guild_ids
)
async def _joke_tts(ctx):
    guild = ctx.guild
    await join(ctx)
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)

    joke_text = await _joke(ctx)
    filename="data/joke.mp3"
    string_to_sound_file(joke_text, filename)
    audio_source = discord.FFmpegPCMAudio(filename)

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=lambda _: rm_joke(filename))

##### Quack Voice #####
@slash.slash(
    name="quack",
    description="Says Quack!",
    guild_ids=guild_ids
)
async def _quack(ctx):
    guild = ctx.guild
    await join(ctx)
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    filename="data/quack.mp3"
    audio_source = discord.FFmpegPCMAudio(filename)
    if not voice_client.is_playing():
        voice_client.play(audio_source)

    await ctx.send("Quack!")

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

# @bot.listen
# async def on_message(message):
#     print(message)
    
bot.run(bot_token)
# client.run(bot_token)