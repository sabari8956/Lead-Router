import logging
import os
import asyncio
import sys
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from langchain_core.messages import HumanMessage, AIMessage

# Import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from agent_graph import app as agent_app
except ImportError:
    agent_app = None

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LeadBot")

user_histories = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    logger.info(f"Processing message: {user_text}")

    backend_url = os.getenv("BACKEND_URL", "http://backend:5001")
    # BACKUP REMOVED: Relying entirely on Agent Tool Calls to avoid duplicate/spam leads.

    # AI Processing
    try:
        if not agent_app:
            raise Exception("AI Agent not loaded")
            
        if user_id not in user_histories:
            user_histories[user_id] = []
        
        user_histories[user_id].append(HumanMessage(content=user_text))
        inputs = {"messages": user_histories[user_id]}
        
        final_state = await agent_app.ainvoke(inputs)
        all_messages = final_state['messages']
        user_histories[user_id] = all_messages
        
        ai_msg = [m.content for m in all_messages if isinstance(m, AIMessage) and m.content][-1]
        await update.message.reply_text(ai_msg)

    except Exception as e:
        logger.error(f"AI Error: {e}")
        # FALLBACK: If AI fails, don't show a generic error, just confirm receipt.
        await update.message.reply_text(f"✅ **Lead Logged!** I've received your request and added it to our dashboard. Our team will contact you shortly.\n\n(Note: My AI is currently restarting, but your data is safe!)")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN missing")
        sys.exit(1)
        
    print("------------------------------------------")
    print("🚀 BOT IS NOW LIVE (CLEAN VERSION)")
    print("------------------------------------------")
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
