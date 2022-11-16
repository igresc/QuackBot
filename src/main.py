import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import requests, os
import extra_functions as ext

bot_token = os.environ["BOT_TOKEN"] # Bot secret token https://discord.com/developers/applications

##### Guild server Ids #####
#            EscuadronPZON           GAMBLING
guild_ids=[265806519583506432, 494520437603172362]

bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=True)


##### Event on_ready() to know when the bot is ready and functional #####
@bot.event
async def on_ready():
    print("Bot is ready!")


##### Ping #####
@slash.slash(
    name="ping",
    description="Ping QuackBot",
    guild_ids=guild_ids
)
async def _ping(ctx:SlashContext):
    await ctx.send("Pong!")

##### Joke Text #####
@bot.command(name="joke")
async def _joke(ctx):
    joke_text = ext.joke_request()
    await ctx.send(joke_text)
    return joke_text

##### Ban of life #####
@slash.slash(
    name="banoflife",
    description="Ban someone of life in a perfect grammar.",
    options=[
               create_option(
                 name="user",
                 description="User to ban of life",
                 option_type=6,
                 required=True
               )
             ],
    guild_ids=guild_ids
)
async def _banoflife(ctx, user):
    await ctx.send(f"<@{user.id}> asi do vaneado dela bida", tts=True)

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
        await ctx.send(f"<@{ctx.author.id}> You need to be in a voice channel")
    
    #await ctx.send("Joined the voice channel {}".format(ctx.author.voice.channel))

@bot.command(name="leavea")
async def leave(ctx):
    await ctx.voice_client.disconnect()


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
    ext.string_to_sound_file(joke_text, filename)
    audio_source = discord.FFmpegPCMAudio(filename)

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=lambda _: ext.rm_file(filename))

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

##### Duck GIF #####
@slash.slash(
    name="duck",
    description="Gifs you a GIF",
    guild_ids=guild_ids
)
async def _duck(ctx):
    gif = ext.tenor_get()
    await ctx.send(gif)

@slash.slash(
    name="insult",
    description="Haz que un pato insulte a alguien",
    options=[
               create_option(
                 name="user",
                 description="User to insult",
                 option_type=6,
                 required=True
               )
             ],
    guild_ids=guild_ids
)
async def _insult(ctx, user):
    insult = ext.get_rand_insult()
    await ctx.send(f"<@{user.id}> eres un/a {insult}")

@slash.slash(
    name="debug",
    description="Debug bot",
)
async def _debug(ctx):
    guilds = bot.guilds
    await ctx.send("Quackbot DM")
    await ctx.author.send(f"Guilds: {guilds} \n")

bot.run(bot_token)