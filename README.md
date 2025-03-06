# DeepSex Chatbot
以 ValueFX9507/Tifa-DeepsexV2-7b-MGRPO 系列模型為基底，專注於色情角色扮演的AI對談機器人。<br>
有API與Discord BOT兩種形式。
優點是文筆和場景描述很不錯，但記憶不長。

--------
## 主要功能

- **與 Tifa-DeepsexV2-7b-MGRPO 模型交互**：使用 Tifa-DeepsexV2-7b-MGRPO 模型來生成回應。
- **文法檔案增加模型的正確輸出**：使用llama_cpp的文法設定增加模型正確回答的機率。
- **上下文記憶**：會根據 `conversation_id` 保留最近的幾次對話。
- **支援簡繁轉換**：透過 OpenCC 將簡體字轉為繁體字。
- **Discord Bot 整合**：能夠在指定頻道內回應訊息。
- **重置上下文**：使用者可輸入 `reset` 來清空當前對話的記錄。
--------
## 安裝與使用
請先在 [這裡下載](https://huggingface.co/collections/ValueFX9507/tifa-deepsexv2-mgrpo-67b0f0e99d15e90f2cfed096) 你需要的模型，建議Q8以上。<br>
在複製專案後將該模型檔案放入此專案資料夾底下，並且在gguf_server.py中把模型檔名改好。

1. 複製專案：
    ```bash
    git clone https://github.com/samttoo22-MewCat/deepsex-chatbot.git
    ```

2. 使用docker建立環境：
    ```bash
    cd deepsex-chatbot/docker
    docker build -t llama_cpp .
    sudo docker run --gpus all -it -p 8063:8063 -v .:/app llama_cpp /bin/bash
    ```

3. 執行API伺服器（可以調整GPU使用量以及模型名稱）：
    ```bash
    cd ..
    python guff_server.py
    ```

3. 執行Discord BOT（可選，記得要換另一個終端）：
    ```bash
    python DCbot.py
    ```
--------
## API 與 Discord機器人 使用方式

本專案的 FastAPI 伺服器在 http://localhost:8063 提供了一個 `/chat` 端點，允許用戶與模型互動。

## API 說明

### **POST /chat**
用於與 AI 進行對話。

#### **請求參數（JSON）**
| 參數名稱              | 類型   | 預設值 | 描述 |
|------------------|------|------|------|
| `conversation_id`  | `str`  | `"default"` | 對話 ID，用於區分不同用戶的對話上下文 |
| `message`  | `str`  | 無 | 使用者發送的訊息 |
| `reset` | `bool` | `False` | 若為 `True` 則清空該對話的上下文 |
| `temperature` | `float` | `0.75` | 控制回應的隨機性，數值越高則越隨機 |
| `max_tokens` | `int` | `2500` | 限制回應的最大字數 |
| `top_p` | `float` | `0.6` | 控制語言模型生成的多樣性 |
| `repeat_penalty` | `float` | `1.3` | 避免模型重複生成相同句子 |
| `character_name` | `str` | `"沫緋"` | 角色的名字 |
| `character_description` | `str` | `預設角色描述（沫緋）` | 角色的詳細描述 |
| `user_name` | `str` | `"小翎"` | 使用者的名字 |
| `user_description` | `str` | `預設使用者描述（沫緋）` | 使用者的詳細描述 |
| `place_description` | `str` | `預設地點描述（沫緋）` | 地點的詳細描述 |

#### **回應範例**
```json
{
  "message": "你好，小翎。我今天過得很不錯，你呢？"
}
```

## Discord Bot 功能

該機器人會監聽指定的 Discord 頻道，並根據用戶的訊息與 API 進行互動。

### 指令

一般聊天：直接輸入訊息，機器人會回應。

reset：輸入 reset，清空當前用戶的對話記錄。

### 設定

請確保 DISCORD_TOKEN 設置正確，並且 ALLOWED_CHANNELS 包含允許機器人回應的頻道 ID。

---------
## 實際展示
![image](https://github.com/user-attachments/assets/03299067-69d9-4f04-8162-cc034f040035)<br>
![image](https://github.com/user-attachments/assets/9f7f5fbe-7a39-437c-b5dc-5551a2f2735f)

## 許可與貢獻

- 「沫緋」的人物設定是由我和丸太共同製作而成。
- 本專案為開源專案，你可以自由使用與修改。
- 如果有任何建議或錯誤回報，請提交 Issue 或 Pull Request。

## 注意事項

- 本專案涉及 NSFW 內容，請謹慎使用。
- 若要在公開 Discord 伺服器中運行，請確保符合 Discord 的使用政策。

## 聯絡方式
Email: v99sam@gmail.com
