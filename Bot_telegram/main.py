from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8044370616:AAHB8zhr13q5kQmeQcaQ03lVpWDfjiFIfbo'

RESPUESTAS = {
    "es": {"hola": "¡Hola!", "chao": "¡Adiós!", "perro": "¡Me gustan los perros!"},
    "en": {"hello": "Hello!", "bye": "Goodbye!", "dog": "I love dogs!"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_user = await context.bot.get_me()
    global USUARIO
    USUARIO = f"@{bot_user.username}"
    await update.message.reply_text(f"Hola, bienvenido!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! ¿Cómo puedo ayudarte?")

async def customize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comando personalizado")

async def messages_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    chat_type = update.message.chat.type

    if chat_type == "group" and USUARIO not in texto:
        return

    if chat_type == "group":
        texto = texto.replace(USUARIO.lower(), "").strip()

    respuesta = answer(texto)
    await update.message.reply_text(respuesta)

def answer(text, lang="es"):
    if lang in RESPUESTAS:
        for clave, respuesta in RESPUESTAS[lang].items():
            if clave in text:
                return respuesta
    return "No tengo respuesta para ello"

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comando no reconocido.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("customize", customize))
    app.add_handler(MessageHandler(filters.TEXT, messages_entry))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_error_handler(error_handler)
    app.run_polling()
