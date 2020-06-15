import discord
from discord.ext import commands

import Utils

from core import logger, fetch_one_line

class Nickname(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.group(aliases=["n"])
  @commands.guild_only()
  async def nickname (self, ctx):
    """
    Nickname manager for RPG sessions.
    """
    if ctx.invoked_subcommand is None:
      await ctx.send ("Use `{}help nickname`".format (ctx.prefix))

  @nickname.command()
  async def set (self, ctx, nickname: str, voiceChannel: discord.VoiceChannel):
    """
    Set a nickname for a specific voice channel (use `"` if you use space in your nickname)
    """
    guild_id                 = ctx.guild.id
    user_id                  = ctx.author.id
    channel_id               = voiceChannel.id
    select                   = 'select count (*) from `nickname_set` where user_id=? and channel_id=? ;'
    data                     = fetch_one_line (select, [user_id, channel_id])
    logger ("nickname::set", "In data: {}".format (data))
    
    
    