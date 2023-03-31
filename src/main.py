import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import os
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
    vc: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    source = discord.FFmpegPCMAudio("data/quack.mp3")
    try:
        channel = ctx.author.voice.channel
        try:
            vc = await channel.connect()
            vc.play(source)
        except discord.errors.ClientException:
            print("Bot already connected to a voice channel.")
            print("Moving to the new channel...")
            await vc.move_to(channel)
            vc.play(source)

    except AttributeError:
        await ctx.send(f"<@{ctx.author.id}> You need to be in a voice channel")
    
    #await ctx.send("Joined the voice channel {}".format(ctx.author.voice.channel))

@bot.command(name="leavea")
async def leave(ctx):
    await ctx.voice_client.disconnect()


##### Joke TTS #####
@slash.slash(
    name="dadjoke",
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
async def quack(ctx):
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
    insult_text = ext.get_rand_insult()
    await join(ctx)
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    insult_frase = f"<@{user.id}> eres un/a {insult_text}"
    await ctx.send(insult_frase)

    filename="data/insult.mp3"
    ext.string_to_sound_file(f"{user.name} eres un/a {insult_text}", filename, lang="es")
    print(f"{user.name} eres un/a {insult_text}")
    audio_source = discord.FFmpegPCMAudio(filename)

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=lambda _: ext.rm_file(filename))

@slash.slash(
    name="debug",
    description="Debug bot",
)
async def _debug(ctx):
    guilds = bot.guilds
    await ctx.send("Quackbot DM")
    await ctx.author.send(f"Guilds: {guilds} \n")
    await ctx.author.send(f"Bot VCs: {bot.voice_clients} \n")

@bot.event
async def on_voice_state_update(member, before, after):
    filename="data/quack.mp3"
    audio_source = discord.FFmpegOpusAudio(filename)
    if not any(x for x in member.roles if x.id == 1075157644005884005):
        return

    channel = after.channel

    if (before.channel == None):
        try:
            vc = await channel.connect()
        except discord.errors.ClientException as e:
            print(e)
    elif (after.channel == None):
        for x in bot.voice_clients:
            if(x.server == before.channel.server):
                await x.disconnect()
    elif (before.channel != after.channel):
        vc: discord.VoiceClient = discord.utils.get(bot.voice_clients)

        print(f"Bot already connected to voice channel: {vc.channel}")
        print("Moving to the new channel...")
        try:
            await vc.move_to(channel)
        except any as e:
            print(e)

    if not vc.is_playing():
        vc.play(audio_source)


bot.run(bot_token)