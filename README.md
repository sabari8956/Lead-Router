# 🚀 Real Estate Lead Management System

A complete full-stack application that bridges Telegram messages to ClickUp tasks with a beautiful real-time dashboard.

## ✨ Features

- 🤖 **Telegram Bot** - AI-powered bot that collects lead information
- 📊 **Real-time Dashboard** - Beautiful web interface to view and manage leads
- 🔄 **ClickUp Integration** - Automatic task creation in ClickUp
- 🎨 **Modern UI** - Premium dark-mode design with gradients and animations
- 📈 **Analytics** - Track lead statistics and performance metrics
- 🔍 **Filtering** - Filter leads by status and priority
- ⚡ **Auto-refresh** - Dashboard updates every 30 seconds

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Telegram  │────────▶│  Python Bot  │────────▶│   ClickUp   │
│     Bot     │         │  (LangGraph) │         │     API     │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                        ▲
                               │                        │
                               ▼                        │
                        ┌──────────────┐                │
                        │  Flask API   │────────────────┘
                        │   (Backend)  │
                        └──────────────┘
                               ▲
                               │
                               │
                        ┌──────────────┐
                        │   Dashboard  │
                        │  (Frontend)  │
                        └──────────────┘
```

## 📋 Prerequisites

- Python 3.9+ (if running without Docker)
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (recommended)
- Telegram Bot Token ([@BotFather](https://t.me/botfather))
- OpenRouter API Key ([openrouter.ai](https://openrouter.ai/))
- ClickUp API Key and List ID (Optional for local mode)

---

## � Getting Started

### Option 1: Docker (Recommended)
This is the easiest way to get everything running in one go.

1. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   TELEGRAM_BOT_TOKEN=your_token
   OPENROUTER_API_KEY=your_key
   CLICKUP_API_KEY=your_key
   CLICKUP_LIST_ID=your_id
   ```

2. **Run with Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the Apps**
   - **Dashboard**: [http://localhost:8000](http://localhost:8000)
   - **Backend API**: [http://localhost:5001](http://localhost:5001)

---

### Option 2: Manual Setup (Run as Code)
Use this if you want to develop or run services individually.

1. **Setup Backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python app.py
   ```
   *Backend runs on `http://localhost:5001`*

2. **Setup Telegram Bot**
   ```bash
   # From root directory
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/bot.py
   ```

3. **Open Frontend**
   Simply open `frontend/index.html` in your browser, or serve it:
   ```bash
   cd frontend
   python3 -m http.server 8000
   ```

---

## 📱 Usage

### Creating a Lead via Telegram

1. Open your Telegram bot
2. Send a message like:
   ```
   Hi, I'm John (0501234567). Looking to buy a villa in Dubai Marina.
   ```
3. The AI bot will:
   - Extract your name, phone, and intent
   - Ask for any missing information
   - Create a task in ClickUp when complete

### Viewing Leads in Dashboard

1. Open the dashboard at `http://localhost:8000`
2. View statistics on the main dashboard
3. Click "All Leads" to see the complete list
4. Filter by status or priority
5. Click "View" to see detailed information
6. Click "Open in ClickUp" to manage the task

## 🎨 Dashboard Features

- **Dashboard View**: Overview with statistics and recent leads
- **All Leads View**: Complete list with filtering options
- **Analytics View**: Performance metrics (coming soon)
- **Auto-refresh**: Updates every 30 seconds
- **Manual Refresh**: Click the refresh button in the header
- **Lead Details**: Click "View" to see full lead information

## 🔑 Getting API Keys

### Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the token provided

### OpenRouter API Key
1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Go to Keys section and create a new key
4. Top up credits if using paid models, or use free models like `google/gemma-3-27b-it:free`

### ClickUp API Key
1. Go to [ClickUp Settings](https://app.clickup.com/settings/apps)
2. Click "Generate" under API Token
3. Copy the token

### ClickUp List ID
1. Open ClickUp and navigate to your list
2. The List ID is in the URL: `https://app.clickup.com/.../{list_id}/...`

## 🛠️ Troubleshooting

### Bot won't start
- Check that `TELEGRAM_BOT_TOKEN` is valid
- Ensure `OPENROUTER_API_KEY` is set correctly

### Dashboard shows no leads
- Make sure the backend API is running on port 5001
- Check browser console for errors
- Verify ClickUp credentials are correct

### Leads not appearing in ClickUp
- Verify `CLICKUP_API_KEY` and `CLICKUP_LIST_ID` are correct
- Check the bot console for error messages

## 📊 Project Structure

```
project/
├── src/                    # Telegram bot source code
│   ├── bot.py             # Main bot application
│   ├── agent_graph.py     # LangGraph AI agent
│   ├── clickup.py         # ClickUp API client
│   └── classifier.py      # Lead classification
├── backend/               # Flask API backend
│   ├── app.py            # API server
│   └── requirements.txt  # Backend dependencies
├── frontend/             # Web dashboard
│   ├── index.html       # Main HTML
│   ├── styles.css       # Premium CSS styles
│   └── app.js           # Dashboard logic
├── .env                 # Environment variables
├── requirements.txt     # Bot dependencies
└── README.md           # This file
```

## 🎯 Next Steps

- [ ] Add real-time notifications using WebSockets
- [ ] Implement user authentication
- [ ] Add charts and visualizations
- [ ] Create mobile-responsive design
- [ ] Add SLA tracking and alerts
- [ ] Implement lead assignment to agents

## 📝 License

This project is for internal use.

## 🤝 Support

For issues or questions, check the console logs or contact your system administrator.

---

**Built with ❤️ using Python, Flask, and modern web technologies**
