from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
from mesh_cipher.core import encrypt, decrypt  # Importa tu algoritmo de cifrado
import re
from typing import Tuple

# Token proporcionado por BotFather
TOKEN = '8089744390:AAET3NX71VKF7lHyhdlY6_Vx52sWDEG4vPs'


def validate_key(key: str) -> Tuple[bool, str]:
    """Valida que la clave no esté vacía."""
    if not key:
        return False, "⚠️ La clave no puede estar vacía."
    return True, "✅ Clave válida."

def validate_message(message: str) -> Tuple[bool, str]:
    """Valida que el mensaje no esté vacío."""
    if not message:
        return False, "⚠️ El mensaje no puede estar vacío."
    return True, "✅ Mensaje válido."

# Función que se ejecuta cuando el bot recibe un mensaje
async def start(update: Update, context: CallbackContext) -> None:
    # Crear botones para "Cifrar" y "Descifrar"
    keyboard = [['Cifrar', 'Descifrar']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        '¡Hola! ¿Qué deseas hacer?\n'
        'Selecciona una opción: "Cifrar" o "Descifrar"',
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip()

    # Verificar el estado de la acción
    action = context.user_data.get('action')

    if action == 'cifrar':
        # Almacenar el mensaje y pedir la clave
        context.user_data['message'] = user_message
        await update.message.reply_text('Ahora, por favor, envíame la clave para cifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.user_data['action'] = 'esperando_clave_cifrar'

    elif action == 'descifrar':
        # Almacenar el mensaje cifrado y pedir la clave
        context.user_data['message'] = user_message
        await update.message.reply_text('Ahora, por favor, envíame la clave para descifrar el mensaje.')

        # Cambiar el flujo para que espere la clave
        context.user_data['action'] = 'esperando_clave_descifrar'

    elif action == 'esperando_clave_cifrar':
        # La clave para cifrar el mensaje
        clave = user_message
        is_valid, validation_msg = validate_key(clave)
        if not is_valid:
            await update.message.reply_text(validation_msg)
            return

        message = context.user_data['message']
        try:
            encrypted_message = encrypt(message, clave)  # Llamamos a encrypt para cifrar el mensaje
            await update.message.reply_text(f"🔒 Mensaje cifrado: {encrypted_message}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        context.user_data.clear()  # Limpiar la información después del cifrado

    elif action == 'esperando_clave_descifrar':
        # La clave para descifrar el mensaje
        clave = user_message
        is_valid, validation_msg = validate_key(clave)
        if not is_valid:
            await update.message.reply_text(validation_msg)
            return

        message = context.user_data['message']
        try:
            decrypted_message = decrypt(message, clave)  # Llamamos a decrypt para descifrar el mensaje
            await update.message.reply_text(f"🔓 Mensaje descifrado: {decrypted_message}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        context.user_data.clear()  # Limpiar la información después del descifrado

    else:
        # Si no hay acción en progreso, debe preguntar la acción a realizar
        if user_message.lower() == "cifrar":
            await update.message.reply_text('Por favor, envíame el mensaje que deseas cifrar.')
            context.user_data['action'] = 'cifrar'

        elif user_message.lower() == "descifrar":
            await update.message.reply_text('Por favor, envíame el mensaje cifrado que deseas descifrar.')
            context.user_data['action'] = 'descifrar'

        else:
            await update.message.reply_text(
                '⚠️ Por favor, selecciona una opción válida: "Cifrar" o "Descifrar".'
            )

# Función principal para iniciar el bot
def main() -> None:
    """Inicializa el bot y empieza a recibir mensajes."""
    application = Application.builder().token(TOKEN).build()

    # Comando /start
    application.add_handler(CommandHandler("start", start))

    # Manejador de mensajes para opciones de cifrado/descifrado
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Empieza el bot
    application.run_polling()  # Llamar directamente a run_polling() sin asyncio.run()

if __name__ == '__main__':
    main()
