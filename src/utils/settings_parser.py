import json

with open('../settings.json') as config_file:
    user_settings = json.load(config_file)
