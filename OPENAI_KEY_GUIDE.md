# How to get your OpenRouter API Key
1.  **Go to OpenRouter**: [https://openrouter.ai/](https://openrouter.ai/)
2.  **Log in** to your account.
3.  Navigate to the **Keys** section.
4.  Click **"Create Key"**.
5.  Copy the key that starts with `sk-or-...`.
6.  Open the `.env` file in this project.
7.  Paste it like this:
    ```env
    OPENROUTER_API_KEY=sk-or-v1-eafedc217a897...
    ```
8.  This project now uses the **Google Gemma 3** model (`google/gemma-3-27b-it:free`) by default.
