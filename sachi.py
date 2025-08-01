import threading
from fastapi import FastAPI
import uvicorn

import discord
from discord.ext import commands, tasks
import os
from discord.utils import get
import random
import re
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import asyncio
from zoneinfo import ZoneInfo

if os.getenv("RENDER") != "true":  # 判斷是否在 Render 環境中
    from dotenv import load_dotenv
    load_dotenv()

# 用你自己的 Token
TOKEN = os.getenv("BOT_TOKEN")
print(TOKEN)
# 設定 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 bot
bot = commands.Bot(command_prefix='!', intents=intents)
JP_scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Tokyo"))
TPE_scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Taipei"))

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
    
MY_USER_ID = 617673911940808706

NORMAL_CHANNEL_ID = 1293206795677995041
DIVINE_CHANNEL_ID = 1400686378156687480
BIRTHDAY_CHANNEL_ID = 1346860688127299654

user_states = {}
said_today = {}

target_chars = ['!', '！', '﹗']
pathetic_keyword = ['婆','可愛','舔', '跟我回家', '喔…', '哦…', '217', '57', '170', '557', 'l70', '201', '515', '486']
sachi_keyword = ['沙知']
banana_keyword = ['蕉']
ki_keyword = ['Ki', 'kI', 'KI', 'ki', 'き', 'キ']
deter_keyword = ["幫我決定"]
divine_keyword = ["我今天的運勢"]
old2_keyword = ["老二"]
kan_keyword = ["Kan", "kan", "かん", "カン", "菅"]

def is_url(text):
    pattern = re.compile(
        r'(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?'
    )
    return bool(pattern.search(text))

def remove_angle_brackets_content(text):
    return re.sub(r"<[^>]*>", "", text)

char_birthdays = {
    "ブッブーですわ! 黑澤黛雅": "01-01",
    "歐羅拉 此花輝夜": "01-03",
    "五桐玲聲優 宮野芹": "01-05",
    "嘉嘉 Liyuu": "01-09",
    "村野・媽媽・蓮之空常識人1號・素顏像素專業翻唱・綴理的鬧鐘・沙耶香": "01-13",
    "小泉花陽": "01-17",
    "此花輝夜聲優 天澤朱音": "01-19",
    "葳恩·西部雅卡農・雌小鬼・瑪格麗特": "01-20",
    "ksks 中須霞": "01-23",
    "山田真綠聲優 小戶森穗花": "01-23",
    "村野沙耶香聲優 野中心菜": "01-28",
    "徒町小鈴聲優 葉山風花": "01-28",
    "朝香果林聲優 久保田未夢": "01-31",
    "東條希聲優 楠田亞衣奈": "02-01",
    "我毫無疑問 艾瑪·薇蒂": "02-05",
    "黑澤黛雅聲優 小宮有紗": "02-05",
    "高海千歌聲優 伊波杏樹": "02-07",
    "抱抱狂魔 松浦果南": "02-10",
    "鹿角聖良聲優 田野麻美": "02-12",
    "麻布麻衣": "02-13",
    "露一手給你看看的鐘嵐珠": "02-15",
    "黑澤露比聲優 降幡愛": "02-19",
    "鬼塚夏美聲優 繪森彩": "02-23",
    "嵐千砂都": "02-25",
    "大場奈奈聲優 小泉萌香": "02-27",
    "徒町・恐龍・ちぇすとー！・ドルケ家的小孩・小鈴": "02-28",
    "雪菜更重要的上原步夢": "03-01",
    "賽馬 金澤奇跡": "03-02",
    "印度舞 國木田花丸": "03-04",
    "只選一個什麼的做不到啊！的矢野妃菜喜": "03-05",
    "嵐千砂都聲優 岬奈子": "03-08",
    "上海的海是海未的海": "03-15",
    "聖澤悠奈聲優 吉武千颯": "03-28",
    "駒形花火聲優 藤野心": "03-31",
    "101期生 舞台少女櫻坂雫": "04-03",
    "鬼塚冬毬聲優 坂倉花": "04-03",
    "調布乃理子": "04-04",
    "先放一邊的櫻小路希奈子": "04-10",
    "若菜四季聲優 大熊和奏": "04-13",
    "初代挺王渡邊曜": "04-17",
    "廠長 相良茉優": "04-17",
    "西木野真姬": "04-19",
    "八岐大蛇進藤天音": "04-20",
    "前田・147・腟壓・酒豪・城之內・佳織里": "04-25",
    "澀谷香音": "05-01",
    "西木野真姬聲優 Pile": "05-02",
    "大西亞玖璃聲優 上原步夢": "05-02",
    "鹿角聖良": "05-04",
    "山田真綠": "05-07",
    "椎名立希聲優 林鼓子": "05-15",
    "葉月戀聲優 青山渚": "05-16",
    "小泉花陽久保ユリカ": "05-19",
    "ちゅけ 榆井希實": "05-21",
    "日野下．小兔子．大木頭．快去跟沙耶香唱素顏像素．吟子跟塞拉斯在爭奪的獎品．フラワー．花帆日野下花帆": "05-22",
    "米雅·泰勒聲優 內田秀": "05-24",
    "宮下愛": "05-30",
    "金澤奇跡聲優 坂野愛羽": "05-31",
    "東條希": "06-09",
    "柊摩央聲優 結木由奈": "06-09",
    "駒形花火": "06-11",
    "小原鞠莉": "06-13",
    "乙宗・蓮之空誘拐犯・海獺操縱者・機械さん的好朋友・肌肉系學園偶像・梢": "06-15",
    "若菜四季": "06-17",
    "佐佐木翔音聲優 涼之瀨葵音": "06-18",
    "塞拉斯・超大・真的超大菲爾德": "06-26",
    "神樂光聲優 三森鈴子": "06-28",
    "我的聲優 小原好美": "06-28",
    "朝香果林": "06-29",
    "蕉的老婆payton尚未": "07-01",
    "五桐玲": "07-09",
    "絢瀨繪里聲優 南條愛乃": "07-12",
    "津島善子": "07-13",
    "唐可可": "07-17",
    "藪島朱音": "07-18",
    "矢澤妮可": "07-22",
    "內田彩": "07-23",
    "鈴木愛奈": "07-23",
    "高海千歌": "08-01",
    "高坂穗乃果": "08-03",
    "法元明菜": "08-05",
    "鬼塚夏美": "08-07",
    "優木雪菜": "08-08",
    "逢田梨香子": "08-08",
    "聖澤悠奈": "08-11",
    "齊藤朱夏": "08-16",
    "高橋波爾卡": "08-18",
    "月音瑚奈": "08-20",
    "佐佐木琴子": "08-28",
    "大澤瑠璃乃": "08-31",
    "村上奈津實": "09-07",
    "南小鳥": "09-12",
    "櫻井陽菜": "09-17",
    "櫻內梨子": "09-19",
    "瀨古梨愛": "09-19",
    "指出毬亞": "09-20",
    "黑澤露比": "09-21",
    "春宮悠可里": "09-22",
    "安養寺姬芽": "09-24",
    "高槻加奈子": "09-25",
    "結那": "09-27",
    "平安名堇": "09-28",
    "伊達小百合": "09-30",
    "遠藤璃菜": "10-04",
    "三船栞子": "10-05",
    "田中千惠美": "10-06",
    "奧村優季": "10-13",
    "鬼頭明里": "10-16",
    "百生吟子": "10-20",
    "絢瀨繪里": "10-21",
    "小林愛香": "10-23",
    "花宮初奈": "10-24",
    "飯田里穗": "10-26",
    "米女芽衣": "10-29",
    "星空凜": "11-01",
    "鈴原希實": "11-01",
    "諏訪奈奈香": "11-02",
    "來栖凜": "11-08",
    "佐佐木翔音": "11-11",
    "天王寺璃奈": "11-13",
    "夕霧綴理": "11-17",
    "菅叶和": "11-19",
    "葉月戀": "11-24",
    "桂城泉": "12-01",
    "柊摩央": "12-02",
    "米雅·泰勒": "12-06",
    "新田惠海": "12-10",
    "鹿角理亞": "12-12",
    "三宅美羽": "12-14",
    "近江彼方": "12-16",
    "藤島慈": "12-20",
    "楠木燈": "12-22",
    "佐藤日向": "12-23",
    "德井青空": "12-26",
    "鬼塚冬毬": "12-28",
    "綾咲穗音": "12-31"
}

async def send_birthday_messages():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    today = now.strftime("%m-%d")
    for name, birthday in char_birthdays.items():
        if birthday == today:
            channel = bot.get_channel(BIRTHDAY_CHANNEL_ID)
            if channel:
                await channel.send(f"🎉今天是{name}的生日，お誕生日おめでとう！🎂")

async def rain_clock():
    channel = bot.get_channel(NORMAL_CHANNEL_ID)
    if channel:
        rain = await bot.fetch_user(497031137177239563)
        if rain:
            await channel.send(f"{rain.mention}快去寫學妹們的文")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    JP_scheduler.add_job(send_birthday_messages, CronTrigger(hour=0, minute=0, timezone=ZoneInfo("Asia/Tokyo")))
    JP_scheduler.start()

    TPE_scheduler.add_job(rain_clock, CronTrigger(hour=21, minute=0, timezone=ZoneInfo("Asia/Taipei")))
    TPE_scheduler.start()

@bot.event
async def on_message(message):
    # 避免回應自己的訊息
    if message.author == bot.user:
        return

    user_id = message.author.id
    channel_id = message.channel.id

    clean_text = remove_angle_brackets_content(message.content):

    if channel_id == DIVINE_CHANNEL_ID:
        now = datetime.now(ZoneInfo("Asia/Taipei"))
        today = now.strftime("%m-%d")

        last_date = said_today.get(user_id)

        if last_date == today:
            await message.reply("你問過了啦 (ノ｀Д´)ノ")
        else:
            said_today[user_id] = today
            choices = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
            reply = random.choice(choices)
            await message.reply(reply)
        return

    # 檢查訊息是否包含特定字符
    if any(char in clean_text for char in target_chars):
        await message.reply(f'你再用驚嘆號試試看')

    if any(char in clean_text for char in pathetic_keyword) and not is_url(message.content):
        guild = bot.get_guild(1293206795677995038) 
        if guild is not None:
            ga = get(guild.emojis, name="word_ga")
            hopeless = get(guild.emojis, name="word_pathetic")
            wake = get(guild.emojis, name="word_xing")
            await message.reply(f'{str(ga)}{str(hopeless)}{str(wake)}')
    
    if any(char in clean_text for char in sachi_keyword):
        if any(char in message.content for char in deter_keyword):
            choices = ["相信的心就是你的魔法", "哇～哈哈哈！我不覺得這是好選項呢！", "なるほど、なるほどね...你自己決定"]
            reply = random.choice(choices)
            await message.reply(reply)
        else:
            if user_id != MY_USER_ID:
                await message.reply(f'不許玩我')

    if any(char in clean_text for char in banana_keyword):
        await message.reply(f'我老公怎麼你了')

    if any(char in clean_text for char in ki_keyword) and not is_url(message.content):
        await message.reply(f'眩耀夜行『ここじゃない』でUO折る人\n・気品がある\n・美男美女\n・頭がいい\n・リーダーシップがある\n・いい匂い\n・陽キャ\n\n『綺麗な夜だね』でUO折る人\n・バカ\n・アホ\n・マヌケ\n・オタンコナス\n・スットコドッコイ\n・臭い\n・陰キャ')
    
    if any(char in clean_text for char in old2_keyword):
        await message.reply(f'你才老二你全家都老二')

    if clean_text == "哇":
        await message.reply("わ わ わ わ わ わ ワールドカオス\n諸行 木暮 時雨 神楽 金剛山 翔襲叉")
    
    if any(char in clean_text for char in kan_keyword) and not is_url(message.content):
        await message.reply("カンカンカンカン菅叶和\nいやいやいやいや菅まどか\n菅叶和 菅叶和\n始球式 パンツ見せ\n水着になれよ 写真集")
    
    # 確保指令也能處理
    await bot.process_commands(message)

# 啟動 bot
bot.run(TOKEN)
