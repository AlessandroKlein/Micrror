from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
import threading
from bot.helper.telegram_helper.bot_commands import BotCommands


def list_drive(update, context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        reply = sendMessage('Buscando..... Espere por favor!', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
        else:
            editMessage(f'No se encontraron resultados para <code>{search}</code>', reply, button)

    except IndexError:
        sendMessage('Envíe una clave de búsqueda junto con el comando', context.bot, update)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
