import threading
from fastapi import FastAPI
import uvicorn
import discord
from discord.ext import commands
import os
from discord.utils import get
import random
import datetime

# 用你自己的 Token
TOKEN = 'MTQwMDQ2Njk3NDkzMjQ3MTkyOQ.GgBs86.37-wLOOB8THujYX_DnkRngeaYc-tu_6LWlMSjE'

# 設定 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)

app = FastAPI()

@app.head("/")
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()

@app.get("/")
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()


# 指定要找的字符（可以多個）
user_states = {}
said_today = {}

target_chars = ['!', '！', '﹗']
pathetic_keyword = ['婆','可愛','舔']
sachi_keyword = ['沙知']
banana_keyword = ['蕉']
ki_keyword = ['ki', 'き']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # 避免回應自己的訊息
    if message.author == bot.user:
        return

    user_id = message.author.id

    # 檢查訊息是否包含特定字符
    if any(char in message.content for char in target_chars):
        await message.reply(f'你再用驚嘆號試試看')

    if any(char in message.content for char in pathetic_keyword):
        guild = bot.get_guild(1293206795677995038) 
        if guild is not None:
            ga = get(guild.emojis, name="word_ga")
            hopeless = get(guild.emojis, name="word_pathetic")
            wake = get(guild.emojis, name="word_xing")
            await message.reply(f'{str(ga)}{str(hopeless)}{str(wake)}')
    
    if message.content == "沙知學姊我今天的運勢" or message.content == "沙知學姐我今天的運勢":
        today = datetime.date.today()

        last_date = said_today.get(user_id)

        if last_date == today:
            await message.reply("你問過了啦 (ノ｀Д´)ノ")
        else:
            said_today[user_id] = today
            choices = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
            reply = random.choice(choices)
            await message.reply(reply)
    elif message.content == '沙知學姊幫我決定一下' or message.content == '沙知學姐幫我決定一下':
        choices = ["相信的心就是你的魔法", "哇～哈哈哈！我不覺得這是好選項呢！", "なるほど、なるほどね...你自己決定"]
        reply = random.choice(choices)
        await message.reply(reply)
    elif any(char in message.content for char in sachi_keyword):
        await message.reply(f'不許玩我')

    if any(char in message.content for char in banana_keyword):
        await message.reply(f'我老公怎麼你了')

    if any(char in message.content for char in ki_keyword):
        await message.reply(f'眩燿夜行『ここじゃない』でUO折る人\n・気品がある\n・美男美女\n・頭がいい\n・リーダーシップがある\n・いい匂い\n・陽キャ\n\n『綺麗な夜だね』でUO折る人\n・バカ\n・アホ\n・マヌケ\n・オタンコナス\n・スットコドッコイ\n・臭い\n・陰キャ')
    

    # 確保指令也能處理
    await bot.process_commands(message)

# 啟動 bot
bot.run(TOKEN)
