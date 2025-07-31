import discord
from discord.ext import commands

# 用你自己的 Token
TOKEN = 'MTQwMDQ2Njk3NDkzMjQ3MTkyOQ.GgBs86.37-wLOOB8THujYX_DnkRngeaYc-tu_6LWlMSjE'

# 設定 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)

# 指定要找的字符（可以多個）
target_chars = ['!', '！']
count = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    global count
    # 避免回應自己的訊息
    if message.author == bot.user:
        return

    # 檢查訊息是否包含特定字符
    if any(char in message.content for char in target_chars):
        count += 1
        await message.reply(f'{count}')

    # 確保指令也能處理
    await bot.process_commands(message)

# 啟動 bot
bot.run(TOKEN)
