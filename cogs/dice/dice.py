import re
import random

import discord
from discord.ext import commands

import Utils

class Dice (commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(aliases=["r"])
  #@commands.guild_only()
  async def roll (self, ctx, *, dice_text: str):
    """
    Make a roll using the server pseudo-radom.
    Usage -roll XdN
    """
    if not re.search ("^(\d+[dD]\d+)", dice_text):
      await ctx.send ("Format {} invalid".format (dice_text))
      return
    match_dice_part = re.search ("(\d+[dD]\d+)", dice_text)
    dice_parts = match_dice_part.group()#.lower().split('d')
    print ("dice_parts: {}".format (dice_parts))
    elements = dice_parts.split ('d')
    print (elements)
    number = int (elements [0])
    face = int (elements [1])
    print ("number: ")
    print (number)
    print ("face: ")
    print (face)
    output                   = ""
    for n in range(number):
      output                 =output+ ("{}" if n ==0 else " | {} ").format(random.randint(1, face))
    await ctx.send (output)
    """
    match_dice_bonus = re.search ("((\+|-)\d+)+", dice_text)
    dice_bonus = 0
    print ("match_dice_bonus")
    print (match_dice_bonus)
    if match_dice_bonus:
      dice_bonus = eval (match_dice_bonus.group ())
    print ("dice_bonus: {}".format (dice_bonus))
    """
