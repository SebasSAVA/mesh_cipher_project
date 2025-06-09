from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
from mesh_cipher.core import encrypt, decrypt  # Importa tu algoritmo de cifrado

# Token proporcionado por BotFather
TOKEN = 'your_bot_token_here'

# Función que se ejecuta cuando el bot recibe un mensaje
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        '¡Hola! ¿Qué deseas hacer?\n'
        '1. Cifrar un mensaje: Envía "cifrar"\n'
        '2. Desencriptar un mensaje: Envía "descifrar"\n'
        'Escribe "cifrar" o "descifrar" para comenzar.'
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    incoming_message = update.message.text.strip().lower()

    # Si el usuario decide cifrar o descifrar
    if incoming_message == "cifrar":
        update.message.reply_text('Por favor, envíame el mensaje que deseas cifrar.')
        context.user_data['action'] = 'cifrar'
    elif incoming_message == "descifrar":
        update.message.reply_text('Por favor, envíame el mensaje cifrado que deseas descifrar.')
        context.user_data['action'] = 'descifrar'
    else:
        update.message.reply_text(
            'Por favor, elige una opción válida: "cifrar" o "descifrar".'
        )

def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip()

    # Verifica si ya se ha seleccionado una acción
    if 'action' not in context.user_data:
        update.message.reply_text(
            'Por favor, escribe "cifrar" o "descifrar" para comenzar.'
        )
        return

    action = context.user_data['action']

    if action == 'cifrar':
        # Almacenar el mensaje y pedir la clave
        context.user_data['message'] = user_message
        update.message.reply_text('Ahora, por favor, envíame la clave para cifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.user_data['action'] = 'esperando_clave_cifrar'

    elif action == 'descifrar':
        # Almacenar el mensaje cifrado y pedir la clave
        context.user_data['message'] = user_message
        update.message.reply_text('Ahora, por favor, envíame la clave para descifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.user_data['action'] = 'esperando_clave_descifrar'

    elif action == 'esperando_clave_cifrar':
        # La clave para cifrar el mensaje
        clave = user_message
        message = context.user_data['message']
        try:
            encrypted_message = encrypt(message, clave)  # Llamamos a encrypt para cifrar el mensaje
            update.message.reply_text(f"Mensaje cifrado: {encrypted_message}")
        except Exception as e:
            update.message.reply_text(f"Error: {str(e)}")
        context.user_data.clear()  # Limpiar la información después del cifrado

    elif action == 'esperando_clave_descifrar':
        # La clave para descifrar el mensaje
        clave = user_message
        message = context.user_data['message']
        try:
            decrypted_message = decrypt(message, clave)  # Llamamos a decrypt para descifrar el mensaje
            update.message.reply_text(f"Mensaje descifrado: {decrypted_message}")
        except Exception as e:
            update.message.reply_text(f"Error: {str(e)}")
        context.user_data.clear()  # Limpiar la información después del descifrado

def main():
    """Inicializa el bot y empieza a recibir mensajes."""
    updater = Updater(TOKEN)

    # Obtiene el dispatcher para registrar los manejadores de comandos y mensajes
    dispatcher = updater.dispatcher

    # Comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Manejador de mensajes
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Manejador para texto y clave
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Empieza el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
