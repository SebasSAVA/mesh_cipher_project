from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mesh_cipher.core import encrypt, decrypt  # Importa tu algoritmo de cifrado

# Token proporcionado por BotFather
TOKEN = '8089744390:AAET3NX71VKF7lHyhdlY6_Vx52sWDEG4vPs'

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
        # Primero el mensaje, luego la clave
        context.user_data['message'] = user_message
        update.message.reply_text('Ahora, por favor, envíame la clave para cifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.user_data['action'] = 'esperando_clave_cifrar'

    elif action == 'descifrar':
        # Primero el mensaje cifrado, luego la clave
        context.user_data['message'] = user_message
        update.message.reply_text('Ahora, por favor, envíame la clave para descifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.us
