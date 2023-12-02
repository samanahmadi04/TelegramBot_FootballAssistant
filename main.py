from pyrogram import Client

plugins = dict(root="plugins")

app = Client('selfbot', api_id=00000000, api_hash='XXXXXXXX',
             bot_token='XXXXXXXXX', plugins=plugins)

print('Bot is running...')
app.run()
