import discord
from discord.ext import commands
import aiohttp
import asyncio

# 請將以下變數依實際狀況調整
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
API_BASE_URL = "http://localhost:8063"  # API 主機與埠號

# 建立 Discord Bot（依需求調整 intents）
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
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