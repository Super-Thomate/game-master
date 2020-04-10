import os
import json

config                       = {}

dir_path                     = os.path.dirname (os.path.realpath (__file__)) + '/'

with open (dir_path+'config.json') as json_file:
  config                     = json.load (json_file)

# print (config)
