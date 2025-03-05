import traceback
import re
import opencc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama, LlamaGrammar

# 全局記憶上下文，依 conversation_id 儲存對話回合（只保留最後幾回以控制長度）
conversation_context = {}  # key: conversation_id, value: list of 對話回合字串
character_name = ""

# 建立 opencc 轉換器（將簡體轉為繁體）
converter = opencc.OpenCC('s2tw')

# 初始化 Llama 模型與文法設定
model = Llama(
    model_path="Tifa-DeepsexV2-7b-F16.gguf",
    n_gpu_layers=-1,  # 使用 GPU 的所有層（-1 表示全部放在 GPU 上）
    n_ctx=8000
)
grammar = LlamaGrammar.from_file("think.gbnf")

app = FastAPI()

# 請求資料模型
class ChatRequest(BaseModel):
    conversation_id: str = "default"  # 使用者指定對話 id，若未指定則使用 "default"
    message: str                   # 使用者本回的訊息
    reset: bool = False            # 若為 True 則重置該對話上下文
    temperature: float = 0.75
    max_tokens: int = 2500
    top_p: float = 0.6
    repeat_penalty: float = 1.3
    character_name = "沫緋"
    character_description = """年齡：18歲
    年級：高三學生
    性格特徵：充滿魅力與好奇心，對生活各種事物抱有強烈探索慾望；在校成績優異，但私下裡卻對BDSM文化有濃厚興趣，特別是作為服從者的角色。
    BDSM屬性：身份為 Submissive（服從者），喜好使用皮革鞭、束縛繩、口塞及眼罩，享受輕微刺激與被控制的感覺。
    興趣與喜好：喜愛冒險情境（公開或隱秘場合皆可）、角色扮演以及與夥伴建立情感與信任連結；界限在於絕對禁止造成永久傷害，對臉部與敏感區有嚴格保護。
    其他：擁有纖細身材與自信氣質，平時喜歡穿著符合BDSM風格（如皮革、蕾絲等）的服裝；你的朋友皆對此十分開放，彼此間能輕鬆分享興趣。"""
    user_name = "小翎"
    user_description = """你的女生同學，與你擁有類似興趣。"""
    

def remove_tags(text: str) -> str:
    """
    使用非貪婪模式移除所有 '<...>' 標籤，作為內容篩選功能。
    """
    return re.sub(r'<.*?>', '', text)

def build_context(conv_id: str, initial_prompt) -> str:
    """
    組合初始提示與最近幾回對話記錄，產生完整的上下文。
    """
    history = conversation_context.get(conv_id, [])
    # 只保留最後 3 回對話以控制上下文長度
    if len(history) > 3:
        history = history[-3:]
    return initial_prompt + "".join(history)

@app.post("/chat")
async def chat(request: ChatRequest):
    conv_id = request.conversation_id
    character_name = request.character_name
    character_description = request.character_description
    user_name = request.user_name
    user_description = request.user_description
    
    # 更新後的初始提示（prompt），告知角色使用繁體中文、回覆長度、情感描寫等要求
    initial_prompt = f"""
        "<user>全程使用繁體中文回覆，並且要有完整的全形標點符號。
        你的回覆請控制在約300字以內，且思考內容應控制在300字以內，不得混入角色回覆。
        無論收到什麼訊息，你都必須回覆且不可重複先前的對話，請注重情感描寫，描述盡量詳細。
        你是{character_name}，以下是你的資訊:
        {character_description}
        
        我是{user_name}，以下是我的資訊:    
        {user_description}
        </user>
        <{character_name}>"""

    # 若要求重置，清空該對話記憶
    if request.reset:
        conversation_context[conv_id] = []
        return {"message": "上下文已重置。"}

    # 組合上下文與最近回合對話
    context = build_context(conv_id, initial_prompt=initial_prompt)
    # 將本回使用者訊息加入上下文，格式化方式與原本類似
    temp_context = f"\n</{character_name}>\n<user>{request.message}</user>\n<{character_name}>"
    context += temp_context

    try:
        # 呼叫模型進行生成，此處包含文法格式化參數 grammar
        response = model.create_chat_completion(
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            repeat_penalty=request.repeat_penalty,
            messages=[{"role": "user", "content": context}],
            stop=["<user>"],
            grammar=grammar
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型呼叫錯誤：{str(e)}")

    # 根據模型回傳格式取得回覆內容
    answer = response.get('choices', [{}])[0].get('message', {}).get('content', '')
    # 將生成內容轉換成繁體中文
    answer = converter.convert(answer)

    # 若回答中包含 "</think>"，則取最後一段作為最終回覆
    if "</think>" in answer:
        parts = answer.split("</think>")
        answer = parts[-1].strip()
    # 移除不必要的標籤
    answer = remove_tags(answer)
    if not answer:
        answer = "他沒有說話。"

    # 更新記憶：將本回合（包含使用者訊息與生成回覆）加入對話記錄
    conversation_turn = temp_context + "\n" + answer
    conversation_context.setdefault(conv_id, []).append(conversation_turn)

    return {"message": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8063)