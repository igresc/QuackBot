import discord
from main import *

@bot.event
async def on_voice_state_update(member, before, after):
    quack()
    # filename="data/quack.mp3"
    # audio_source = discord.FFmpegOpusAudio(filename)
    # if not any(x for x in member.roles if x.id == 1075157644005884005):
    #     return

    # channel = after.channel

    # if (before.channel == None):
    #     try:
    #         vc = await channel.connect()
    #     except discord.errors.ClientException as e:
    #         print(e)
        
    #     if not vc.is_playing():
    #         vc.play(audio_source)

    # elif (after.channel == None):
    #     # for x in bot.voice_clients:
    #     if(bot.voice_clients.server == before.channel.server):
    #         await bot.voice_clients.disconnect()
    # elif (before.channel != after.channel):
    #     vc: discord.VoiceClient = discord.utils.get(bot.voice_clients)

    #     print(f"Bot already connected to voice channel: {vc.channel}")
    #     print("Moving to the new channel...")
    #     try:
    #         await vc.move_to(channel)
    #     except any as e:
    #         print(e)

    #     if not vc.is_playing():
    #         vc.play(audio_source)