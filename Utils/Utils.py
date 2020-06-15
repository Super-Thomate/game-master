import inspect
import json
import math
import os
import re
import sys
import time
from threading import Timer as _Timer
from functools import wraps
from urllib.request import urlopen
from core.Logger import logger

import botconfig

import emoji
import discord

from discord.ext.commands import BadArgument, EmojiConverter
from discord.ext import commands


def require(required: list):
  def decorator(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
      ctx = args[1]
      
      return await f(*args, **kwargs)

    return decorated

  return decorator




def format_time(timestamp):
  timer = [["j", 86400]
    , ["h", 3600]
    , ["m", 60]
    , ["s", 1]
           ]
  current = timestamp
  logger ("Utils::format_time", f"current: {current}")
  to_ret = ""
  for obj_time in timer:
    if math.floor(current / obj_time[1]) > 0:
      to_ret += str(math.floor(current / obj_time[1])) + obj_time[0] + " "
      current = current % obj_time[1]
  if not len(to_ret):
    logger ("Utils::format_time", "to ret is empty")
  return to_ret.strip()


def has_role(member, role_id):
  try:
    for obj_role in member.roles:
      if obj_role.id == int(role_id):
        return True
  except Exception as e:
    logger ("Utils::has_role", f"{type(e).__name__} - {e}")
  return False


def parse_time(timestr):
  units = {   "j": 86400
            , "h": 3600
            , "m": 60
            , "s": 1
          }
  to_ret = 0
  number = 0
  for elem in timestr:
    try:
      cast = int(elem)
    except Exception:
      # is it a letter in units ?
      if elem not in units:
        raise Exception(f"Unknown element: {elem}")
      to_ret = to_ret + number * units[elem]
      number = 0
    else:
      number = number * 10 + cast
  return to_ret



def debug(message):
  """
  Debug function, to use rather than print (message)
  https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
  """
  info = inspect.getframeinfo((inspect.stack()[1])[0])
  print(sys._getframe().f_lineno)
  print(info.filename, 'func=%s' % info.function, 'line=%s:' % info.lineno, message)


def is_valid_url(url):
  regex = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
  return url is not None and regex.search(url)


def is_url_image(image_url):
  if not is_valid_url(image_url):
    return False
  image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
  try:
    site = urlopen(image_url)
    meta = site.info()  # get header of the http request
  except Exception as e:
    logger ("Utils::is_url_image", f"{type(e).__name__} - {e}")
    return False
  return meta["content-type"] in image_formats


def convert_str_to_time(time_string):
  time_array = time_string.split(" ")
  logger ("Utils::convert_str_to_time", f"time_array: {time_array}")
  timestamp = 0
  current = 0
  for element in time_array:
    logger ("Utils::convert_str_to_time", f"element: {element}")
    if element.isnumeric():
      current = int(element)
      logger ("Utils::convert_str_to_time", f"isnumeric = current: {current}")
    else:
      if element == "months":
        current = current * 28 * 24 * 3600
      elif element == "weeks":
        current = current * 7 * 24 * 3600
      logger ("Utils::convert_str_to_time", f"else current: {current}")
      timestamp = timestamp + current
      current = 0
  logger ("Utils::convert_str_to_time", f"timestamp: {timestamp}")
  return timestamp

async def delete_messages(*args):
  for msg in args:
    await msg.delete(delay=2)


def is_custom_emoji(emoji_text: str):
  split = emoji_text.split(':')
  if len(split) == 3:
    return split[2][:-1]  # remove '>' at the end
  return None

def is_emoji (character: str):
  return character in emoji.UNICODE_EMOJI

async def get_emoji (ctx: commands.Context, emoji: str):
  try:
    converter              = EmojiConverter ()
    return await converter.convert (ctx, emoji)
  except BadArgument:
    if is_emoji (emoji):
    	 return emoji
    else:
    	 raise

def emojize (character: str):
  return emoji.emojize (character, use_aliases=True)

def demojize (character: str):
  return emoji.demojize (character)

def setInterval(timer, task, *args):
  isStop                     = task()
  if not isStop:
    _Timer(timer, setInterval, [timer, task, args]).start()

async def confirm_command (message: discord.Message, status: bool):
  reaction                   = emojize (':white_check_mark:') if status else emojize (':x:')
  try:
    await message.add_reaction (reaction)
  except Exception as e:
    logger ("Utils::confirm_command", f"{type(e).__name__} - {e}")