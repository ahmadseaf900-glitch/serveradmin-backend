import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from python_aternos import Client_Aternos

# إعدادات الـ Logs لمعرفة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# جلب البيانات من إعدادات Render الأمنية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

# الاتصال بـ Aternos عبر الكوكي لتخطي الحماية
try:
    aternos = Client_Aternos.from_session(ATERNOS_SESSION)
    myserver = aternos.list_servers()[0] # السيرفر الأول في الحساب
    print("✅ تم الاتصال بـ Aternos بنجاح!")
except Exception as e:
    print(f"❌ فشل الاتصال بـ Aternos: {e}")

# أوامر البوت
async def start_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري تشغيل السيرفر...")
    try:
        myserver.start()
        await update.message.reply_text("🚀 تم إرسال أمر التشغيل!")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

async def status_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        myserver.fetch() # تحديث البيانات
        await update.message.reply_text(f"📊 حالة السيرفر الحالية: {myserver.status}")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ في جلب الحالة: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # ربط الأوامر
    app.add_handler(CommandHandler("start_mc", start_server))
    app.add_handler(CommandHandler("status", status_server))
    
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()

