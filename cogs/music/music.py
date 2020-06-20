# based on https://stackoverflow.com/questions/56060614/how-to-make-a-discord-bot-play-youtube-audio
import math
import time
from datetime import datetime

import discord
from discord.ext import commands
import youtube_dl

import Utils
import botconfig

from core import logger

import os
import glob

dir_path                     = os.path.dirname(os.path.realpath(__file__)) + '/'

class Music (commands.Cog):
  def __init__(self, bot):
    self.bot                 = bot
    self.volume              = 0.6

  @commands.group(aliases=["m"])
  @commands.guild_only()
  async def music (self, ctx):
    """
    Discord music player. Upload a song or play it from youtube.
    """
    if ctx.invoked_subcommand is None:
      await ctx.send ("Use `{}help music`".format (ctx.prefix))

  @music.command(aliases=["y"])
  async def yplay (self, ctx, *, url):
    """
    Download a youtube soundtrack in mp3 and plays it. Usage: -m y <url>
    """
    logger ("music::yplay", url)
    voice_state = ctx.author.voice
    if voice_state is None:
      await ctx.send ("Not in a voice channel ?")
      return
    # already connected ?
    if not ctx.guild.voice_client:
      logger ("music::yplay", "not connected: establishing a connection")
      voice_channel = voice_state.channel
      if voice_channel is None:
        await ctx.send ("No voice channel")
        return
      voice_client = await voice_channel.connect()
    else:
      logger ("music::yplay", "already connected") 
      voice_client = ctx.guild.voice_client
    stream = False
    logger ("music::yplay", "start download")
    async with ctx.typing():
      player                 = await YTDLSource.from_url(url, loop=self.bot.loop, stream=stream)
      logger ("music::yplay", "download source")
      if voice_client.is_playing():
        voice_client.stop()
        logger ("music::yplay", "already on play")
      voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
      logger ("music::yplay", "launch song")
    await ctx.send('Now playing: {}'.format(player.title))
    logger ("music::yplay", "Now playing")

  @music.command(aliases=["yd", "download"])
  async def ydownload (self, ctx, *, url):
    """
    Download a youtube soundtrack in mp3. Usage: -m yd <url>
    """
    logger ("music::ydownload", url)
    player                 = await YTDLSource.from_url(url, loop=self.bot.loop)
    logger ("music::ydownload", "download source")
    await ctx.send('Now playing: {}'.format(player.title))
    logger ("music::ydownload", "Now playing")


  @music.command(aliases=["p"])
  async def play (self, ctx, *, name):
    """
    Play a mp3 file already on the server. Usage: -m p <title>
    """
    logger ("music::play", name)
    voice_state = ctx.author.voice
    if voice_state is None:
      await ctx.send ("Not in a voice channel ?")
      return
    # already connected ?
    if not ctx.guild.voice_client:
      logger ("music::play", "not connected: establishing a connection")
      voice_channel = voice_state.channel
      if voice_channel is None:
        await ctx.send ("No voice channel")
        return
      voice_client = await voice_channel.connect()
    else:
      logger ("music::play", "already connected")
      voice_client = ctx.guild.voice_client
    logger ("music::play", "start download")
    async with ctx.typing():
      player                 = discord.FFmpegPCMAudio (name+'.mp3')
      logger ("music::play", "download source")
      if voice_client.is_playing():
        voice_client.stop()
        logger ("music::play", "already on play")
      """
      voice_client.source = discord.PCMVolumeTransformer(player)
      voice_client.source.volume = self.volume
      """
      voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

      logger ("music::play", "launch song")
    await ctx.send('Now playing: {}'.format(name+'.mp3'))
    logger ("music::play", "Now playing")

  @music.command(aliases=["a"])
  async def pause(self, ctx):
    """
    Pause current music. Usage: -m a
    """
    if not ctx.guild.voice_client:
      return
    else:
      voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
      voice_client.pause()
      await ctx.send ("Player paused")

  @music.command(aliases=["r"])
  async def resume(self, ctx):
    """
    Resume current music. Usage: -m r
    """
    if not ctx.guild.voice_client:
      return
    else:
      voice_client = ctx.guild.voice_client
    if not voice_client.is_playing():
      voice_client.resume()
      await ctx.send ("Player resumed")

  @music.command(aliases=["s"])
  async def stop(self, ctx):
    """
    Stop current music. Usage: -m s
    """
    if not ctx.guild.voice_client:
      return
    else:
      voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
      voice_client.stop()
      await ctx.send ("Player stopped")

  @music.command(aliases=["d"])
  async def disconnect (self, ctx):
    """
    Disconnect bot from VoiceChannel. Usage: -m d
    """
    if not ctx.guild.voice_client:
      return
    else:
      voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
      voice_client.stop()
      await ctx.send ("Player stopped")
    await voice_client.disconnect()
    await ctx.send ("Good bye !")

  @music.command(aliases=["l"])
  async def list (self, ctx):
    """
    List mp3 file available. Usage: -m l
    """
    lists_file               = []
    list_file                = ""
    for file in glob.glob("*.mp3"):
      list_file += file.split(".")[0]+"\n"
      if len (list_file) > 1000:
        lists_file.append("```\n{}```".format (list_file))
        list_file            = ""
    if len(list_file):
      lists_file.append("```\n{}```".format (list_file))
    if not len (lists_file):
      await ctx.send ("```\nNo music file found```")
      return
    for list_to_send in lists_file:
      await ctx.send (list_to_send)

  @music.command(aliases=["u"])
  async def upload (self, ctx):
    """
    Upload a mp3 file. Usage: -m u
    Upload is a 2 steps process
    """
    await ctx.send ("Send a mp3 file")
    def check (m):
      logger ("music::upload", "check message")
      return m.channel == ctx.channel and len (m.attachments)
    message                  = await self.bot.wait_for ('message', check=check)
    files                    = message.attachments
    for file in files:
      file_name              = file.filename
      logger ("music::upload", "file: {}".format(file_name))
      extension              = os.path.splitext(file_name)[1]
      logger ("music::upload", "extension: {}".format(extension))
      if extension == ".mp3":
        try:
          bytes              = await file.save (file_name)
          logger ("music::upload", "saved {} bytes".format(bytes))
        except Exception as e:
          await ctx.send (f"{type(e).__name__} - {e}")
        await ctx.send ("Uploaded "+file_name)
    await message.delete (delay=1)

  @music.command(aliases=["sec1"])
  async def secret1 (self, ctx):
    """
    Play a secret music 1
    """
    #name = "Gealdyr_-_Loki"
    name = "Go_bwah"
    voice_state = ctx.author.voice
    if voice_state is None:
      await ctx.send ("Not in a voice channel ?")
      return
    # already connected ?
    if not ctx.guild.voice_client:
      logger ("music::play", "not connected: establishing a connection")
      voice_channel = voice_state.channel
      if voice_channel is None:
        await ctx.send ("No voice channel")
        return
      voice_client = await voice_channel.connect()
    else:
      logger ("music::play", "already connected")
      voice_client = ctx.guild.voice_client
    logger ("music::play", "start download")
    async with ctx.typing():
      player                 = discord.FFmpegPCMAudio (name+'.mp3')
      logger ("music::play", "download source")
      if voice_client.is_playing():
        voice_client.stop()
        logger ("music::play", "already on play")
      """
      voice_client.source = discord.PCMVolumeTransformer(player)
      voice_client.source.volume = self.volume
      """
      voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

      logger ("music::play", "launch song")
    await ctx.send('`OK`')
    logger ("music::play", "Now playing")

  def play_music(self, ctx: commands.Context, name: str):
    voice_client             = ctx.guild.voice_client
    player                   = discord.FFmpegPCMAudio (name+'.mp3')
    voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else self.play_music(ctx,name))

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'download_archive': 'archive.txt'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
      loop = loop or asyncio.get_event_loop()
      data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

      if 'entries' in data:
          # take first item from a playlist
          data = data['entries'][0]
      print ("filename: {}".format (ytdl.prepare_filename(data)))
      filename = data['url'] if stream else ytdl.prepare_filename(data)
      return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)