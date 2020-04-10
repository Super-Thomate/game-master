"""
_Cron.py
Manage functions for automatic process
"""
import asyncio
# IMPORT
import math
import random
import time
from datetime import datetime

import discord
from crontab import CronTab

import Utils

from .Logger import logger
 

async def run_task (bot, task, interval):
  await bot.wait_until_ready()
  cron = CronTab(interval)
  while True:
    try:
      await asyncio.sleep(cron.next(default_utc=True))
    except Exception as e:
      logger ("_Cron::run_task", f"task {task} => {type(e).__name__} - {e}")
    try:
      if task == "":
        return
    except:
      logger ("_Cron::run_task", f'I could not perform task `{task}` :(')
