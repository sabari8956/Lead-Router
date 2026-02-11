# 🚀 Quick Start Guide

## Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

## Step 2: Verify Your .env File

Make sure your `.env` file has all required credentials:

```env
TELEGRAM_BOT_TOKEN=8403293963:AAGim-jxjZ9luTHQEsrvQpeM1UrxBRH3Rpk
OPENROUTER_API_KEY=sk-or-v1-...
CLICKUP_API_KEY=B4Q4MQ45EHN8XJW5ASMLUHPCULTMSRR8
CLICKUP_LIST_ID=3RXQDG2V8XPKLVLU20A1BDSQ4UQSA6PCD5N544FIU9CQY626EEW6AVVH628U9JT
```

## Step 3: Start Everything

### Option A: Use the Startup Script (Recommended)

**Windows PowerShell:**
```powershell
.\start.ps1
```

**Windows Command Prompt:**
```cmd
start.bat
```

### Option B: Start Manually

**Terminal 1 - Telegram Bot:**
```bash
python src/bot.py
```

**Terminal 2 - Backend API:**
```bash
cd backend
python app.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
python -m http.server 8000
```

## Step 4: Test the System

1. **Open Dashboard**: http://localhost:8000
2. **Send Telegram Message**: 
   - Open your Telegram bot
   - Send: "Hi, I'm John (0501234567). Looking to buy a villa."
3. **Watch the Magic**:
   - Bot will ask for any missing info
   - Task will be created in ClickUp
   - Dashboard will show the new lead (refresh or wait 30 seconds)

## 🎉 That's It!

You now have a complete lead management system running!

## 📊 What You'll See

- **Telegram Bot**: Collects lead information intelligently
- **ClickUp**: Tasks are created automatically
- **Dashboard**: Beautiful UI showing all your leads in real-time

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
cd backend
pip install -r requirements.txt
```

### Dashboard shows "Error loading data"
- Make sure backend is running on port 5000
- Check browser console (F12) for errors

### Bot not responding
- Verify TELEGRAM_BOT_TOKEN is correct
- Check that OPENROUTER_API_KEY is set

## 📞 Need Help?

Check the main README.md for detailed documentation.
