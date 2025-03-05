import discord
from discord.ext import commands
import aiohttp
import asyncio

# 請依照實際狀況調整
DISCORD_TOKEN = ""
API_BASE_URL = "http://localhost:8063"  # API 主機與埠號

# 允許 bot 發言的頻道 ID
ALLOWED_CHANNELS = [1338000000027708458, 1214584100000405954]  # 請填入允許的頻道 ID

# 建立 Discord Bot（注意需開啟 message_content 權限）
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 檢查器：只允許在特定頻道或私訊中使用
def is_allowed_channel():
    async def predicate(ctx):
        # 若是在私訊，ctx.guild 為 None，直接允許
        if ctx.guild is None:
            return True
        # 若在公會，檢查頻道 ID 是否在允許清單中
        return ctx.channel.id in ALLOWED_CHANNELS
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"已成功登入：{bot.user} (ID: {bot.user.id})")
    # 嘗試向每個指定頻道發送通知訊息
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

@bot.event
async def on_command_error(ctx, error):
    # 若因檢查失敗而拒絕命令，回覆錯誤訊息
    if isinstance(error, commands.CheckFailure):
        await ctx.send("此頻道不允許使用此命令，請至指定頻道或透過私訊使用。")
    else:
        # 其他錯誤仍由預設錯誤處理機制處理
        raise error

@bot.command()
@is_allowed_channel()
async def chat(ctx, *, user_message: str):
    """
    使用 !chat 指令將使用者訊息轉發給 API，並將回應結果送回 Discord。
    """
    payload = {
        "conversation_id": str(ctx.author.id),
        "message": user_message,
        "reset": False,
        "temperature": 0.75,
        "max_tokens": 2500,
        "top_p": 0.6,
        "repeat_penalty": 1.3,
        "character_name": "沫緋",
        "character_description": """年齡：18歲
        年級：高三學生
        性格特徵：充滿魅力與好奇心，對生活各種事物抱有強烈探索慾望；在校成績優異，但私下裡卻對BDSM文化有濃厚興趣，特別是作為服從者的角色。
        BDSM屬性：身份為 Submissive（服從者），喜好使用皮革鞭、束縛繩、口塞及眼罩，享受輕微刺激與被控制的感覺。
        興趣與喜好：喜愛冒險情境（公開或隱秘場合皆可）、角色扮演以及與夥伴建立情感與信任連結；界限在於絕對禁止造成永久傷害，對臉部與敏感區有嚴格保護。
        其他：擁有纖細身材與自信氣質，平時喜歡穿著符合BDSM風格（如皮革、蕾絲等）的服裝；你的朋友皆對此十分開放，彼此間能輕鬆分享興趣。""",
        "user_name": "小翎",
        "user_description": "你的女生同學，與你擁有類似興趣。"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload) as resp:
                if resp.status != 200:
                    await ctx.send("API 請求錯誤。")
                    return
                data = await resp.json()
                answer = data.get("message", "沒有收到回覆。")
                await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"發生錯誤：{str(e)}")

@bot.command()
@is_allowed_channel()
async def reset(ctx):
    """
    使用 !reset 指令請求 API 重置對話記憶。
    """
    payload = {
        "conversation_id": str(ctx.author.id),
        "message": "",  # 不需傳入訊息內容
        "reset": True,
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
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_BASE_URL}/chat", json=payload) as resp:
                if resp.status != 200:
                    await ctx.send("API 請求錯誤。")
                    return
                await ctx.send("對話記憶已重置。")
        except Exception as e:
            await ctx.send(f"發生錯誤：{str(e)}")

bot.run(DISCORD_TOKEN)