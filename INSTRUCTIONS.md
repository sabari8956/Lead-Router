# ⚠️ ACTION REQUIRED: Enable AI Agent

I have upgraded the bot to use **LangChain/LangGraph** as requested! 🚀

## Critical Step
The AI needs a brain. You must add your **OpenAI API Key** to the `.env` file:

1.  Open `c:\Users\sajan\.gemini\antigravity\scratch\project\.env`
2.  Add:
    ```env
    OPENAI_API_KEY=sk-proj-your-actual-key-here
    ```
3.  Restart the bot:
    ```bash
    python src/bot.py
    ```

## What's New?
-   The bot now **understands context**.
-   It will **ask follow-up questions** if info is missing.
-   It only saves to ClickUp when ready.
