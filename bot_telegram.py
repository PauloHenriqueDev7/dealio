import telebot
from telebot import types
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8123063608:AAFU7sXtfcEGCrCwJ6x9imSvtDHWKR9K5fQ"
bot = telebot.TeleBot(TOKEN)

# --- Função de scraping (adicione sua implementação real) ---
def raspar_cupons_amazon():
    # Simulação (substitua pela sua lógica real)
    return [
        {"loja": "AMAZON", "desconto": "30% OFF", "titulo": "Eletrônicos", "link": "https://amzn.to/42OMp5v"},
        {"loja": "MAGALU", "desconto": "50% OFF", "titulo": "Celulares", "link": "https://produto.magalu.com/SEU_CODIGO"}
    ]

# --- Teclados ---
def criar_teclado_principal():
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🛍️ CUPONS EM DESTAQUE")
        btn2 = types.KeyboardButton("🔎 BUSCAR POR LOJA")
        btn3 = types.KeyboardButton("💎 OFERTAS EXCLUSIVAS")
        markup.add(btn1, btn2, btn3)
        return markup
    except Exception as e:
        logger.error(f"Erro ao criar teclado: {e}")
        return None

# --- Handlers ---
@bot.message_handler(commands=['start', 'help'])
def start(message):
    try:
        teclado = criar_teclado_principal()
        if teclado:
            bot.send_message(
                message.chat.id,
                "✨ *BOTÃO DE CUPONS* ✨\nEscolha uma opção abaixo:",
                parse_mode="MarkdownV2",
                reply_markup=teclado
            )
    except Exception as e:
        logger.error(f"Erro no /start: {e}")

@bot.message_handler(commands=['teste'])
def teste_amazon(message):
    cupons = raspar_cupons_amazon()  # Chama a função de scraping
    if cupons:
        for cupom in cupons[:3]:
            resposta = f"""
            🏷️ *{cupom['loja']}* 🏷️
            🔥 *{cupom['desconto']}* 
            📌 {cupom['titulo']}
            🛒 [Comprar agora]({cupom['link']})
            """
            bot.send_message(message.chat.id, resposta, parse_mode="MarkdownV2")
    else:
        bot.reply_to(message, "❌ Nenhum cupom encontrado.")

@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    try:
        if message.text == "🛍️ CUPONS EM DESTAQUE":
            bot.send_message(message.chat.id, "🔍 Buscando cupons... (implemente a lógica aqui)")
        
        elif message.text == "🔎 BUSCAR POR LOJA":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("AMAZON", "MAGALU", "VOLTAR")
            bot.send_message(message.chat.id, "🔎 Escolha uma loja:", reply_markup=markup)
        
        elif message.text == "VOLTAR":
            bot.send_message(message.chat.id, "Retornando...", reply_markup=criar_teclado_principal())
    
    except Exception as e:
        logger.error(f"Erro: {e}")

if __name__ == "__main__":
    print("Bot iniciado. Envie /start no Telegram.")
    bot.polling()