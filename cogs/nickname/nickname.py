import os

from discord.ext import commands

import Utils

from core import logger

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
    guild_id                 = ctx.guild.id
    
    