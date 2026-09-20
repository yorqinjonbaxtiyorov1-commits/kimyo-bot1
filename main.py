import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# Bosqichlar (State)
NAME, HOMEWORK = range(2)

# Render portini tinglovchi kichik veb-server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# /start bosilganda
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum!\nIltimos, ism va familiyangizni kiriting:")
    return NAME

# Ism-familiya qabul qilinganda
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data['full_name'] = user_name
    
    await update.message.reply_text(
        f"Rahmat, {user_name}!\nEndi uy vazifangizni yuboring (matn, rasm yoki fayl ko'rinishida):"
    )
    return HOMEWORK

# Uy vazifasi qabul qilinganda va ustozga (sizga) yuborilganda
async def get_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = context.user_data.get('full_name', 'O\'quvchi')
    admin_id = os.environ.get("ADMIN_ID") # Sizning Telegram ID raqamingiz

    # 1. O'quvchiga tasdiq xabari
    await update.message.reply_text("✅ Uy vazifangiz ustozga muvaffaqiyatli yetkazildi!")

    # 2. Ustozga (Sizga) xabar yo'naltirish
    if admin_id:
        try:
            # Avval o'quvchi haqida ma'lumot yuboramiz
            student_info = (
                f"📥 **Yangi uy vazifasi!**\n\n"
                f"👤 **O'quvchi:** {user_name}\n"
                f"🆔 **Telegram username:** @{update.effective_user.username if update.effective_user.username else 'Yo\'q'}"
            )
            await context.bot.send_message(chat_id=admin_id, text=student_info, parse_mode="Markdown")
            
            # Keyin o'quvchi yuborgan uy vazifasi (fayl/rasm/matn) ni ustozga yo'naltiramiz
            await update.message.forward(chat_id=admin_id)
        except Exception as e:
            print(f"Xabarni admin ga yuborishda xatolik: {e}")

    # Muloqotni yakunlash
    return ConversationHandler.END

# Bekor qilish komandasi
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Jarayon bekor qilindi. Qaytadan boshlash uchun /start bosing.")
    return ConversationHandler.END

if __name__ == '__main__':
    # Veb-serverni fonda ishga tushirish
    threading.Thread(target=run_web_server, daemon=True).start()

    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    # ConversationHandler yaratamiz
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            HOMEWORK: [MessageHandler(filters.ALL & ~filters.COMMAND, get_homework)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    print("Bot ishga tushdi...")
    app.run_polling()
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Render portini tinglovchi kichik veb-server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# /start buyrug'i uchun javob
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Ism-familiyangiz va uy vazifangizni yuboring.")

# Barcha matnli xabarlarga va fayllarga javob beruvchi funksiya
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Bu yerda foydalanuvchiga tasdiqlash xabari yuboriladi
    await update.message.reply_text("✅ Uy vazifangiz ustozga muvaffaqiyatli yetkazildi!")

if __name__ == '__main__':
    # Veb-serverni fonda ishga tushirish
    threading.Thread(target=run_web_server, daemon=True).start()

    # Botni ishga tushirish
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    # Handlerlarni ulaymiz
    app.add_handler(CommandHandler("start", start))
    
    # Oddiy matnlar hamda rasm/hujjatlar kelganda javob qaytarish
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, handle_message))
    
    print("Bot ishga tushdi...")
    app.run_polling()
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render port kutganda unga OK (200) javobini qaytaruvchi kichik veb-server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Bot buyruqlari
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Bot muvaffaqiyatli ishga tushdi.")

if __name__ == '__main__':
    # Veb-serverni alohida oqimda (thread) ishga tushiramiz
    threading.Thread(target=run_web_server, daemon=True).start()

    # Telegram botni ishga tushirish
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Bot ishga tushdi...")
    app.run_polling()
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

NAME = 0

# BOT TOKEN VA SIZNING TELEGRAM ID'INGIZ:
BOT_TOKEN = "8927870856:AAE22Y0N-B9AzIAEqTM6dnvAPae0wc6je60"
TEACHER_ID = 6420660423  # <--- BU YERGA @userinfobot ORQALI OLGAN ID'INGIZNI YOZING!

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'student_name' not in context.user_data:
        await update.message.reply_text(
            "Assalomu alaykum! Kimyo darsidan uy vazifalarini topshirish botiga xush kelibsiz.\n\n"
            "Iltimos, **Ism va Familiyangizni** kiriting:"
        )
        return NAME
    else:
        await update.message.reply_text(
            f"Xush kelibsiz, {context.user_data['student_name']}!\n"
            "Uy vazifangiz rasmi yoki faylini yuborishingiz mumkin. Men uni ustozga yetkazaman."
        )
        return ConversationHandler.END

async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    student_name = update.message.text
    context.user_data['student_name'] = student_name
    await update.message.reply_text(
        f"Rahmat, {student_name}! Ismingiz saqlandi.\n\n"
        "Endi uy vazifangiz (rasm, PDF yoki fayl)ni yuborishingiz mumkin."
    )
    return ConversationHandler.END

async def handle_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    student_name = context.user_data.get('student_name', update.effective_user.full_name)
    username = update.effective_user.username
    user_link = f"@{username}" if username else f"ID: {update.effective_user.id}"
    
    caption_text = f"📥 **Yangi uy vazifasi keldi!**\n\n👤 **O'quvchi:** {student_name}\n🔗 **Profil:** {user_link}"
    
    if update.message.photo:
        photo_file = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=TEACHER_ID,
            photo=photo_file,
            caption=caption_text,
            parse_mode="Markdown"
        )
    elif update.message.document:
        doc_file = update.message.document.file_id
        await context.bot.send_document(
            chat_id=TEACHER_ID,
            document=doc_file,
            caption=caption_text,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Iltimos, uy vazifasini rasm yoki fayl shaklida yuboring.")
        return

    await update.message.reply_text("✅ Uy vazifangiz ustozga muvaffaqiyatli yetkazildi!")

async def change_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yangi **Ism va Familiyangizni** kiriting:")
    return NAME

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('ism', change_name)
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_homework))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
