import threading
from fastapi import FastAPI
import uvicorn
import discord
from discord.ext import commands
import os
from discord.utils import get

# 用你自己的 Token
TOKEN = 'MTQwMDQ2Njk3NDkzMjQ3MTkyOQ.GgBs86.37-wLOOB8THujYX_DnkRngeaYc-tu_6LWlMSjE'

# 設定 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)

app = FastAPI()

@app.get("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()

# 指定要找的字符（可以多個）
target_chars = ['!', '！', '﹗']
pathetic_keyword = ['我婆','老婆','好可愛']
sachi_keyword = ['沙知']
banana_keyword = ['蕉']
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

    guild = bot.get_guild(1234567890) 
    ga = get(message.guild.emojis, name="word_ga")
    hopeless = get(message.guild.emojis, name="word_pathetic")
    wake = get(message.guild.emojis, name="word_xing")
    if any(char in message.content for char in pathetic_keyword):
        await message.reply(f'{str(ga)}{str(hopeless)}{str(wake)}')

    if any(char in message.content for char in sachi_keyword):
        await message.reply(f'不許玩我')

    if any(char in message.content for char in banana_keyword):
        await message.reply(f'我老公怎麼你了')

    # 確保指令也能處理
    await bot.process_commands(message)

# 啟動 bot
bot.run(TOKEN)
