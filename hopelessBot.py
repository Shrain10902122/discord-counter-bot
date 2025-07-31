import discord
from discord.ext import commands
import os
from discord.utils import get

# 用你自己的 Token
TOKEN = 'MTQwMDQ5MzIzOTgwNjQ2NDEwMg.Gbp1J3.8otqU1MM24xsy3xkgN7Rx8ubWFZMWEi7_yor2M'

# 設定 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)

# 指定要找的字符（可以多個）
target_chars = ['我婆']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # 避免回應自己的訊息
    if message.author == bot.user:
        return

    # 檢查訊息是否包含特定字符
    ga = get(message.guild.emojis, name="word_ga")
    hopeless = get(message.guild.emojis, name="word_pathetic")
    wake = get(message.guild.emojis, name="word_xing")
    if any(char in message.content for char in target_chars):
        await message.reply(f'{str(ga)}{str(hopeless)}{str(wake)}')

    # 確保指令也能處理
    await bot.process_commands(message)

# 啟動 bot
bot.run(TOKEN)
