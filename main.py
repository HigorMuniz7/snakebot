import asyncio
import random
import threading
from flask import Flask
from telegram import Bot
from telegram.constants import ChatAction

# === CONFIGURAÇÕES ===
TOKEN = "7836456161:AAGUi37b9PcqMOTOUI9wCj6_WXqnE-9l7-s"
CHAT_ID = "@crsnakesinais"
bot = Bot(token=TOKEN)

# === CORES DISPONÍVEIS ===
cores = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣']

# === TEMPOS (em segundos) ===
TEMPO_PARA_RESULTADO = 122
TEMPO_PARA_AGUARDE = 125
DURACAO_AGUARDE = 60
APAGAR_ANTES_SINAL = 2

# === Servidor Flask para manter Replit ativo ===
app = Flask(__name__)


@app.route('/')
@app.route('/ping')
def ping():
    return "✅ SnakeBot está online!", 200


def run_flask():
    app.run(host='0.0.0.0', port=8080)


# === Funções do bot ===
async def digitar(segundos=2):
    await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.TYPING)
    await asyncio.sleep(segundos)


async def enviar_sinal():
    cor = random.choice(cores)
    await digitar()
    mensagem = (
        "🐍 *NOVO SINAL DETETADO PELA I.A!* 🔥\n"
        "[📲 REGISTA-TE NO SNAKEBET 🐍](https://slitherbet.com/register)\n"
        f"🎯 *Cor para comer:* {cor}\n"
        f"💸 *META:* € 100\n"
        "⚠️ Após comeres a cor indicada, aguarda o próximo sinal da I.A.")
    await bot.send_message(chat_id=CHAT_ID,
                           text=mensagem,
                           parse_mode="Markdown")


async def enviar_resultado():
    await digitar()
    chance = random.uniform(0, 100)
    if chance <= 98.4:
        await bot.send_photo(chat_id=CHAT_ID,
                             photo="https://i.imgur.com/WJqlXzZ.png")
    else:
        await bot.send_message(chat_id=CHAT_ID,
                               text="❌ *DEU RED* ❌",
                               parse_mode="Markdown")


async def enviar_mensagem_aguarde():
    await digitar()
    return await bot.send_message(
        chat_id=CHAT_ID,
        text=
        "🔎 A Inteligência Artificial está buscando por um novo sinal, por favor, aguarde...",
        parse_mode="Markdown")


async def main():
    await digitar()
    await bot.send_message(chat_id=CHAT_ID,
                           text="🤖 SnakeBet iniciado com sucesso!",
                           parse_mode="Markdown")

    while True:
        await enviar_sinal()
        await asyncio.sleep(TEMPO_PARA_RESULTADO)
        await enviar_resultado()
        await asyncio.sleep(TEMPO_PARA_AGUARDE - TEMPO_PARA_RESULTADO)
        mensagem_aguarde = await enviar_mensagem_aguarde()
        await asyncio.sleep(DURACAO_AGUARDE - APAGAR_ANTES_SINAL)
        await bot.delete_message(chat_id=CHAT_ID,
                                 message_id=mensagem_aguarde.message_id)
        await asyncio.sleep(APAGAR_ANTES_SINAL)


# === Inicialização com suporte ao Flask ===
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    asyncio.run(main())
