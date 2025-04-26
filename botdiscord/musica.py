import discord
from discord.ext import commands
import yt_dlp
import asyncio
import json
import os


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot("n!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="n!play")
    await bot.change_presence(activity=activity)
    print (f"Bot conectado como {bot.user}")

queues = {}

def play_next(guild_id):
    if guild_id in loop_status and loop_status[guild_id]:
        # Reinsere a música atual no início da fila para repetir
        if queues[guild_id]:
            queues[guild_id].insert(0, queues[guild_id][0])

    if queues[guild_id]:
        next_song = queues[guild_id].pop(0)
        voice_client = next_song['voice_client']
        voice_client.play(
            discord.FFmpegPCMAudio(next_song['url'], **{'options': '-vn'}),
            after=lambda e: play_next(guild_id)
        )
        asyncio.run_coroutine_threadsafe(
            next_song['ctx'].send(f"🎶 Tocando: **{next_song['title']}** ({next_song['duration']})"),
            bot.loop
        )

@bot.command(name="p")
async def p(ctx, *, busca: str):
    if not ctx.author.voice:
        await ctx.send("Você não está conectado em uma call")
        return

    canal = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        voice_client = await canal.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(busca, download=False)['entries'][0]
        url_audio = info['url']
        title = info.get('title', 'música')
        duration = info.get('duration', 0)
        duration_fmt = f"{duration // 60}:{duration % 60:02}"

    song = {
        'url': url_audio,
        'title': title,
        'duration': duration_fmt,
        'voice_client': voice_client,
        'ctx': ctx
    }

    guild_id = ctx.guild.id
    if guild_id not in queues:
        queues[guild_id] = []

    if not voice_client.is_playing():
        queues[guild_id].insert(0, song)  # garante que será tocada agora
        play_next(guild_id)
    else:
        queues[guild_id].append(song)
        await ctx.send(f"➕ Adicionada à fila: **{title}** ({duration_fmt})")


@bot.command(name='stop')
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        if voice_client.is_playing():
            voice_client.stop()

        await voice_client.disconnect()
        await ctx.send("⏹️ Música parada e bot desconectado.")
    else:
        await ctx.send("❌ O bot não está conectado em nenhum canal de voz.")

@bot.command(name='skip')
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client or not voice_client.is_playing():
        await ctx.send("❌ Nenhuma música está sendo tocada agora.")
        return

    await ctx.send("⏭️ Pulando para a próxima música...")
    voice_client.stop()  # Isso ativa o `after` no `play`, que já chama a próxima da fila

# Variável global para armazenar o estado de loop por servidor
loop_status = {}

@bot.command(name='loop', help="Ativa ou desativa o loop da música atual")
async def loop(ctx):
    guild_id = ctx.guild.id

    # Alterna o estado do loop
    if guild_id in loop_status and loop_status[guild_id]:
        loop_status[guild_id] = False
        await ctx.send("🔁 Loop desativado.")
    else:
        loop_status[guild_id] = True
        await ctx.send("🔁 Loop ativado.")

@bot.command(name='fila')
async def fila(ctx):
    guild_id = ctx.guild.id
    if guild_id not in queues or not queues[guild_id]:
        await ctx.send("📭 A fila está vazia.")
        return

    fila_texto = ""
    for i, musica in enumerate(queues[guild_id]):
        fila_texto += f"**{i+1}.** {musica['title']} ({musica['duration']})\n"

    embed = discord.Embed(title="🎵 Fila de músicas", description=fila_texto, color=0x1DB954)
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('não encontramos esse comando')
    else:
        raise error #para o bot n dar erro quando não reconhecer um comando


bot.run("")