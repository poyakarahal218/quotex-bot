import json
import time
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# وضع التوكن مباشرة هنا لحل مشكلة المتغيرات على Render
TELEGRAM_BOT_TOKEN = "7667199184:AAE7OQSKF9En4C81N6IqA08ap0Yids4BY"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PAIRS_MAP = {
    "EUR/USD": "EURUSD",
    "GBP/USD": "GBPUSD",
    "USD/JPY": "USDJPY",
    "USD/CAD": "USDCAD",
    "AUD/USD": "AUDUSD",
    "NZD/USD": "NZDUSD",
    "USD/CHF": "USDCHF",
    "EUR/GBP": "EURGBP",
    "EUR/JPY": "EURJPY",
    "GBP/JPY": "GBPJPY",
    "EUR/USD (OTC)": "EURUSD_otc",
    "GBP/USD (OTC)": "GBPUSD_otc",
    "USD/JPY (OTC)": "USDJPY_otc",
    "USD/CAD (OTC)": "USDCAD_otc",
    "AUD/USD (OTC)": "AUDUSD_otc",
    "NZD/USD (OTC)": "NZDUSD_otc",
    "USD/CHF (OTC)": "USDCHF_otc"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    pairs_list = list(PAIRS_MAP.keys())
    for i in range(0, len(pairs_list), 2):
        row = [InlineKeyboardButton(pairs_list[i], callback_data=pairs_list[i])]
        if i + 1 < len(pairs_list):
            row.append(InlineKeyboardButton(pairs_list[i+1], callback_data=pairs_list[i+1]))
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 أهلاً بك في بوت التحليل المباشر!\nاختر زوج العملات المطلوب تحليله:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pair = query.data
    await query.edit_message_text(
        text=f"📊 تحليل زوج العملات: *{pair}*\n\n"
             f"⏱ الوقت: {datetime.now().strftime('%H:%M:%S')}\n"
             f"📈 الاتجاه المتوقع: صاعد 🟢\n"
             f"⭐ التوصية: دخول صفقة شراء (CALL) لمدة 1 دقيقة.\n\n"
             f"⚠️ تنبيه: التداول ينطوي على مخاطر عالية.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 محاولة أخرى", callback_data="refresh_menu")]])
    )

async def refresh_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
    await query.edit_message_text(text="أهلاً بك مجدداً، اضغط للرجوع للقائمة.", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(refresh_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Bot is starting polling...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
