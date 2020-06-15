import discord
from discord.ext import commands

import Utils

from core import logger, fetch_one_line, execute_order

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
    order                    = 'insert into nickname_set (nickname, user_id, channel_id ) values (?, ?, ?) ; '
    select                   = 'select count (*) from `nickname_set` where user_id=? and channel_id=? ;'
    data                     = fetch_one_line (select, [user_id, channel_id])
    if data [0]:
      order                  = 'update nickname_set set nickname=? where user_id=? and channel_id=? ;'
    try:
      execute_order (order, [nickname, user_id, channel_id])
    except Exception as e:
      logger ("nickname::set", "{} - {}".format (type (e).__name__, e))
      await Utils.confirm_command (ctx.message, False)
      return
    await ctx.send ("Nickname set to `{}`".format (nickname))
    await Utils.confirm_command (ctx.message, True)

  @nickname.command()
  async def get (self, ctx, voiceChannel: discord.VoiceChannel = None):
    """
    Get nickname for a specific voice channel or all channel if none provided
    """
    guild_id                 = ctx.guild.id
    user_id                  = ctx.author.id
    if voiceChannel is not None:
      channel_id             = voiceChannel.id
      select                 = 'select nickname from `nickname_set` where user_id=? and channel_id=? ;'
      data                   = fetch_one_line (select, [user_id, channel_id])
      logger ("nickname::set", "data: {}".format (data))
      if data is not None:
        nickname             = data [0]
        await ctx.send ("Nickname for {}: `{}`".format (voiceChannel.name, nickname))
      else:
        await ctx.send ("No nickname for {}".format (voiceChannel.name))
    else:
      # do it for all
      await ctx.send ("WIP")
    await Utils.confirm_command (ctx.message, True)