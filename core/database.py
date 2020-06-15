import os
import sqlite3
import sys
from core import logger

# get the path to sqlite3 db
path                         = os.path.dirname(os.path.realpath(__file__)) + '/../garden.db'

def execute_order(sql, params=[]):
  cnx = sqlite3.connect(path)
  cursor = cnx.cursor()
  logger ("database::execute_order", f"execute_order params: {params}")
  try:
    cursor.execute(sql, (params))
    cnx.commit()
    cursor.close()
  except Exception as e:
    cursor.close()
    logger ("database::execute_order", f' ERROR: {type(e).__name__} - {e}')
    logger ("database::execute_order", f' sql: {sql}')
  cnx.close()

def fetch_one_line(sql, params=[]):
  cnx = sqlite3.connect(path)
  cursor = cnx.cursor()
  line = None
  try:
    cursor.execute(sql, (params))
    line = cursor.fetchone()
    cursor.close()
  except Exception as e:
    cursor.close()
    logger ("database::fetch_one_line", f' ERROR: {type(e).__name__} - {e}')
    logger ("database::fetch_one_line", f' sql: {sql}')
  cnx.close()
  return line


def fetch_all_line(sql, params=[]):
  cnx = sqlite3.connect(path)
  cursor = cnx.cursor()
  lines = None
  try:
    cursor.execute(sql, (params))
    lines = cursor.fetchall()
    cursor.close()
  except Exception as e:
    cursor.close()
    logger ("database::fetch_all_line", f' ERROR: {type(e).__name__} - {e} in \n{sql}')
  cnx.close()
  return lines

def create_table():
  cnx = sqlite3.connect(path)
  cursor = cnx.cursor()
  try:
    ### NICKNAME COG
    cursor.execute (
                      'CREATE TABLE IF NOT EXISTS `nickname_set` ('+
                      '`user_id` INTEGER NOT NULL, '+
                      '`channel_id` INTEGER NOT NULL, '+
                      '`nickname` TEXT NOT NULL, '+
                      'PRIMARY KEY (`user_id`, `channel_id`)'+
                      ') ;'
                   )
    # Save modifications
    103907580723617792
    18446744073709551615
    cnx.commit()
    cursor.close()
  except Exception as e:
    cursor.close()
    logger ("database::create_table", f'ERROR: {type(e).__name__} - {e}')
  cnx.close()