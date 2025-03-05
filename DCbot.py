import discord
import aiohttp
import asyncio

# 請依照實際狀況調整
DISCORD_TOKEN = "你的 Discord Token"
API_BASE_URL = "http://localhost:8063"  # API 主機與埠號

# 允許 bot 處理的頻道 ID（私訊的情況下，message.guild 為 None）
ALLOWED_CHANNELS = [123456789012345678, 987654321098765432]  # 請填入允許的頻道 ID

# 建立 Discord Bot（注意需開啟 message_content 權限）
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"已成功登入：{bot.user} (ID: {bot.user.id})")
    # 向每個指定頻道發送啟動通知
    for channel_id in ALLOWED_CHANNELS:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            try:
                await channel.send("機器人已啟動並進入運作中！")
                print(f"已在頻道 {channel.name} (ID: {channel.id}) 發送啟動通知。")
            except Exception as e:
                print(f"發送訊息到頻道 ID {channel_id} 時出錯：{e}")
        else:
            print(f"找不到頻道 ID：{channel_id}")

async def send_api_request(payload, channel, author):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload) as resp:
                if resp.status != 200:
                    error_msg = "API 請求錯誤。"
                    await channel.send(error_msg)
                    print(f"[{author}] 回應失敗: {error_msg}")
                    return
                data = await resp.json()
                answer = data.get("message", "沒有收到回覆。")
                await channel.send(answer)
                print(f"[{author}] 已發送訊息到 {channel}: {answer}")
        except Exception as e:
            err_str = f"發生錯誤：{str(e)}"
            await channel.send(err_str)
            print(err_str)

@bot.event
async def on_message(message):
    # 忽略機器人自己的訊息
    if message.author.bot:
        return

    # 如果是公會訊息，檢查頻道是否在允許清單內；私訊則直接允許
    if message.guild is not None and message.channel.id not in ALLOWED_CHANNELS:
        return

    # 印出收到的訊息
    print(f"收到來自 {message.author} 的訊息: {message.content}")

    # 定義共用的 payload 內容
    common_payload = {
        "conversation_id": str(message.author.id),
        "temperature": 0.75,
        "max_tokens": 2500,
        "top_p": 0.6,
        "repeat_penalty": 1.3,
        "character_name": "沫緋",
        "character_description": (
            "年齡：18歲\n"
            "年級：高三學生\n"
            "性格特徵：充滿魅力與好奇心，對生活各種事物抱有強烈探索慾望；在校成績優異，但私下裡卻對BDSM文化有濃厚興趣，特別是作為服從者的角色。\n"
            "BDSM屬性：身份為 Submissive（服從者），喜好使用皮革鞭、束縛繩、口塞及眼罩，享受輕微刺激與被控制的感覺。\n"
            "興趣與喜好：喜愛冒險情境（公開或隱秘場合皆可）、角色扮演以及與夥伴建立情感與信任連結；界限在於絕對禁止造成永久傷害，對臉部與敏感區有嚴格保護。\n"
            "其他：擁有纖細身材與自信氣質，平時喜歡穿著符合BDSM風格（如皮革、蕾絲等）的服裝；你的朋友皆對此十分開放，彼此間能輕鬆分享興趣。"
        ),
        "user_name": "小翎",
        "user_description": "你的女生同學，與你擁有類似興趣。"
    }

    # 若訊息為 "reset"，則執行重置操作
    if message.content.lower().strip() == "reset":
        payload = common_payload.copy()
        payload.update({
            "message": "",  # 重置時不需要訊息內容
            "reset": True,
        })
        print(f"收到來自 {message.author} 的重置命令")
        await send_api_request(payload, message.channel, message.author)
    else:
        # 將一般訊息視為聊天內容
        payload = common_payload.copy()
        payload.update({
            "message": message.content,
            "reset": False,
        })
        await send_api_request(payload, message.channel, message.author)

bot.run(DISCORD_TOKEN)