import sys

import discord
from discord.ext import commands

import botconfig

# IMPORT FOR AUTOBOT
from core import run_task, logger

# DISCORD_CRON_CRONTAB         = {}

prefix = ["!", "-"]

# Define all of our cogs
initial_extensions = [   'cogs.dice'
                       , 'cogs.loader'
                       , 'cogs.music'
                       , 'cogs.timer'
                       , 'cogs.nickname'
                     ]

bot = commands.Bot(command_prefix=prefix)
# bot.remove_command("help")  # we used our own help command

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)



@bot.event
async def on_ready():
  logged_in_as               = "Logged in as {0} [{1}]".format (bot.user.name, bot.user.id)
  discord_version            = "Discord.py version {0}".format(discord.__version__)
  len_logged_in_as           = len (logged_in_as)
  len_discord_version        = len (discord_version)
  discord_version            = discord_version + (" " * (len_logged_in_as-len_discord_version))
  dash                       = "----"+("-"*len_logged_in_as)

  login                      = (   "{0}\n"
                                   "| {1} |\n"
                                   "{0}\n"
                                   "| {2} |\n"
                                   "{0}\n"
                               ).format (dash, logged_in_as,  discord_version)
  print(login)
  try:
    await bot.change_presence(activity=discord.Game(name=botconfig.config['activity']))
  except TypeError as type_err:
    logger ("bot::on_ready", "Error TypeError : {}".format(type_err))
    sys.exit(0)
  except Exception as e:
    logger ("bot::on_ready", f"{type(e).__name__} - {e}")
    sys.exit(0)
  """
  # AUTOBOT
  try:
    for task in DISCORD_CRON_CRONTAB:
      interval               = DISCORD_CRON_CRONTAB [task]
      logger ("bot::on_ready::autobot", "Scheduling {0} with intervall [{1}]".format (task, interval))
      bot.loop.create_task (run_task (bot, task, interval))
  except Exception as e:
    logger ("bot::on_ready::autobot", f"{type(e).__name__} - {e}")
    sys.exit(0)
  """

@bot.event
async def on_command_error(ctx: commands.Context, exception):
  logger ("bot::on_command_error", f"ctx.message.content: {ctx.message.content}")
  logger ("bot::on_command_error", f"ctx.args: {ctx.args}")
  logger ("bot::on_command_error", f"ctx.command_failed: {ctx.command_failed}")
  print(exception)
  if not ctx.command:
    return
  await ctx.channel.send(exception)


bot.run(botconfig.config['token'])
