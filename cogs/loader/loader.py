import os

from discord.ext import commands

import Utils

from core import logger, create_table

class Loader (commands.Cog):
  def __init__ (self, bot):
    self.bot                 = bot

  # Hidden means it won't show up on the default help.
  @commands.command ()
  async def load (self, ctx, *, cog: str):
    """
    Load a cog (if not already loaded).
    """
    cog                      = cog.lower ()
    try:
      self.bot.load_extension (f'cogs.{cog}')
    except Exception as e:
      await ctx.send ("**`ERROR:`** {0} - {1}".format (type (e).__name__, e))
    else:
      await ctx.send ("**`SUCCESS`**")

  @commands.command ()
  async def unload (self, ctx, *, cog: str):
    """
    Unload a cog (if not already loaded).
    """
    cog                      = cog.lower ()
    try:
      self.bot.unload_extension (f'cogs.{cog}')
    except Exception as e:
      await ctx.send ("**`ERROR:`** {0} - {1}".format (type (e).__name__, e))
    else:
      await ctx.send ("**`SUCCESS`**")

  @commands.command ()
  async def reload (self, ctx, *, cog: str):
    """
    Reload a cog.
    """
    cog                      = cog.lower()
    try:
      self.bot.unload_extension (f'cogs.{cog}')
      self.bot.load_extension (f'cogs.{cog}')
    except Exception as e:
      await ctx.send ("**`ERROR:`** {0} - {1}".format (type (e).__name__, e))
    else:
      await ctx.send ("**`SUCCESS`**")

  @commands.command ()
  async def cogs (self, ctx):
    """
    Command which lists all loaded cogs
    """
    all_loaded               = ""
    for name in self.bot.cogs.keys ():
      all_loaded            += f"- **{name}**\n"
    if not len(all_loaded):
      all_loaded             = "**NONE**"
    try:
      await ctx.send (all_loaded)
    except Exception as e:
      logger ("loader::list_load", '{0} - {1}'.format (type (e).__name__, e))

  @commands.command (aliases = ['db'])
  async def database (self, ctx):
    """
    Launch the creation of database tables
    """
    try:
      create_table ()
    except Exception as e:
      logger ("loader::list_load", '{0} - {1}'.format (type (e).__name__, e))

