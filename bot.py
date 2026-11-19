from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

historico = {}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto_original = update.message.text or ""
    texto = texto_original.strip().lower()

    if "cfg1io7dd7tcuwrnq3uxxe" in texto:
        return

    # BLOQUEIO DE LINKS
    links_proibidos = [
        "t.me/",
        "https://t.me/",
        "http://t.me/",
        "telegram.me/",
        "joinchat/",
        "chat.whatsapp.com/"
    ]

    for link in links_proibidos:
        if link in texto:

            await update.message.delete()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Links para grupos não são permitidos."
            )
            return

    usuario = update.effective_user.id

    if usuario not in historico:
        historico[usuario] = {
            "ultima": texto,
            "contador": 1
        }
        return

    if texto == historico[usuario]["ultima"]:
        historico[usuario]["contador"] += 1
    else:
        historico[usuario]["ultima"] = texto
        historico[usuario]["contador"] = 1

    if historico[usuario]["contador"] >= 4:

        await update.message.delete()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Evite repetir a mesma mensagem várias vezes."
        )

print("Bot iniciado!")

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        responder
    )
)

app.run_polling(close_loop=False)