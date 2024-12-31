import pandas as pd
import numpy as np
import yfinance as yf
import talib
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن و آی‌دی عددی شما
BOT_TOKEN = "7594441218:AAGSDKd323gG58eLErwvYBrfp5wqi2wEk2I"
ADMIN_ID = 858420539

# تنظیمات ربات
bot = Bot(token="7594441218:AAGSDKd323gG58eLErwvYBrfp5wqi2wEk2I")

# تابع برای ارسال پیام به ادمین
def send_to_admin(context: CallbackContext, message: str):
    context.bot.send_message(chat_id=ADMIN_ID, text=message)

# لیست اندیBکاتورها و وزن‌ها
INDICATORS = {
    'RSI': 1.0,
    'MACD': 1.0,
    'SMA': 1.0,
    'EMA': 1.0,
    'ADX': 1.0,
    'CCI': 1.0,
    'BOLL': 1.0,
    'ATR': 1.0,
    'STOCH': 1.0,
    'WILLR': 1.0
}

# تابع محاسبه سیگنال
def calculate_signals(data):
    signals = []

    # RSI
    rsi = talib.RSI(data['Close'], timeperiod=14)
    if rsi.iloc[-1] > 70:
        signals.append("RSI: Overbought (Sell)")
    elif rsi.iloc[-1] < 30:
        signals.append("RSI: Oversold (Buy)")

    # MACD
    macd, macdsignal, macdhist = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    if macd.iloc[-1] > macdsignal.iloc[-1]:
        signals.append("MACD: Bullish (Buy)")
    else:
        signals.append("MACD: Bearish (Sell)")

    # سایر اندیکاتورها (SMA، EMA، BOLL، و ...)
    # اضافه کنید بر اساس نیاز خود

    return signals

# تابع /start
def start(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        update.message.reply_text("سلام! شما ادمین هستید. از دستورات استفاده کنید.")
    else:
        update.message.reply_text("شما دسترسی به این ربات ندارید.")

# تابع ارسال سیگنال‌ها
def send_signals(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        symbol = context.args[0] if context.args else 'AAPL'
        try:
            data = yf.download(symbol, period="1mo", interval="1d")
            signals = calculate_signals(data)
            message = f"Signals for {symbol}:\n" + "\n".join(signals)
            update.message.reply_text(message)
        except Exception as e:
            update.message.reply_text(f"خطایی رخ داد: {e}")
    else:
        update.message.reply_text("شما اجازه این کار را ندارید.")

# تنظیمات و شروع ربات
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # دستورات ربات
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('signals', send_signals))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()