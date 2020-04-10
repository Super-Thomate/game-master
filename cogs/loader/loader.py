import os

from discord.ext import commands

import Utils

from core import logger

class Loader(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Hidden means it won't show up on the default help.
  @commands.command(name='load', hidden=True)
  async def do_load_cog(self, ctx, *, cog: str):
    """
    Load a cog for Garden
    """
    cog = cog.lower()
    try:
      self.bot.load_extension(f'cogs.{cog}')
    except Exception as e:
      await ctx.send("**`ERROR:`** {0} - {1}".format(type(e).__name__, e))
    else:
      await ctx.send("**`SUCCESS`**")

  @commands.command(name='unload', hidden=True)
  async def do_unload_cog(self, ctx, *, cog: str):
    """
    Unload a cog for Garden
    """
    cog = cog.lower()
    try:
      self.bot.unload_extension(f'cogs.{cog}')
    except Exception as e:
      await ctx.send("**`ERROR:`** {0} - {1}".format(type(e).__name__, e))
    else:
      await ctx.send("**`SUCCESS`**")

  @commands.command(name='reload', hidden=True)
  async def do_reload_cog(self, ctx, *, cog: str):
    """
    Reload a cog for Garden
    """
    cog = cog.lower()
    try:
      self.bot.unload_extension(f'cogs.{cog}')
      self.bot.load_extension(f'cogs.{cog}')
    except Exception as e:
      await ctx.send("**`ERROR:`** {0} - {1}".format(type(e).__name__, e))
    else:
      await ctx.send("**`SUCCESS`**")

  @commands.command(name='cogs', hidden=True)
  async def list_load(self, ctx):
    """
    Command which lists all loaded cogs
    """
    all_loaded = ""
    for name in self.bot.cogs.keys():
      all_loaded += f"- **{name}**\n"
    if not len(all_loaded):
      all_loaded = "**NONE**"
    try:
      await ctx.send(all_loaded)
    except Exception as e:
      logger ("loader::list_load", f'{type(e).__name__} - {e}')

