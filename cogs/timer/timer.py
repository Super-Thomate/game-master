import discord
from discord.ext import commands

import Utils

import core._Timer as _Timer

import time
import asyncio
from core import logger

class Timer(commands.Cog):
  """
  Timer cog: get a visual countdown
  """

  def __init__(self, bot):
    self.bot = bot

  @commands.group(aliases = ["t"])
  @commands.guild_only()
  async def timer (self, ctx: commands.Context,  duration_str: str):
    """
    Launch a countdown for <duration_str>.
    <duration_str> must be in the form XjXhXmXs.
    Example: 1j2h5m32s =w 1 day 2 housr 5 minutes 32 seconds
    """
    try:
      duration               = Utils.parse_time(duration_str)
      if duration < 1:
        await ctx.send ("Duration must be a positive integer !")
        return
      start                  = time.time()
      # GET EMOJI
      emoji                  = Utils.emojize (":red_circle:")
      # GET END MESSAGE
      end_message            = "**Time's Up !**"
      global emoji_row_length
      emoji_row_length       = duration if duration <= 10 else 10
      emoji_row              = (str (emoji)+" " ) * emoji_row_length
      msg_timer              = await ctx.send (emoji_row)
      lag                    = 0.2
      interval               = duration / emoji_row_length - lag

      async def times_up():
        logger ("timer::launch", "times_up -> time : {:.1f}s".format(time.time()-start))
        await ctx.send  (end_message)
        # await msg_timer.edit (content=end_message)

      async def times_up_2():
        logger ("timer::launch", "Time's up ! -> time : {:.1f}s".format(time.time()-start))
        await ctx.send ("Time's up ! -> time : {:.1f}s".format(time.time()-start))

      async def rebuild ():
        #proc_start = time.time()
        global emoji_row_length
        emoji_row_length     = emoji_row_length - 1
        emoji_row            = (str (emoji)+" " ) * emoji_row_length
        if emoji_row_length:
          await msg_timer.edit (content=emoji_row)
          if time.time()-start < duration:
            next_task         = _Timer (interval, rebuild)
        else:
          logger ("timer::launch", "rebuild -> time : {:.1f}s".format(time.time()-start))
        #logger ("timer::launch", time.time()-proc_start)

      #reftimer               = _Timer (duration, times_up_2) # Reference Timer
      timer                  = _Timer (duration, times_up)
      next_task              = _Timer (interval, rebuild)
      await ctx.message.delete(delay=0.5)
    except Exception as e:
      await ctx.send (f"{type(e).__name__} - {e}")
      return
