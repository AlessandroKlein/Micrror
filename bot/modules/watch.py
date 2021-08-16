from telegram.ext import CommandHandler
from telegram import Bot, Update
from bot import DOWNLOAD_DIR, dispatcher, LOGGER
from bot.helper.telegram_helper.message_utils import sendMessage, sendStatusMessage
from .mirror import MirrorListener
from bot.helper.mirror_utils.download_utils.youtube_dl_download_helper import YoutubeDLHelper
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
import threading


def _watch(bot: Bot, update, isTar=False):
    mssg = update.message.text
    message_args = mssg.split(' ')
    name_args = mssg.split('|')
    
    try:
        link = message_args[1]
    except IndexError:
        msg = f"/{BotCommands.WatchCommand} [youtube-dl supported link] [quality] |[CustomName] para reflejar con youtube-dl.\n\n"
        msg += "<b>Nota: la calidad y el nombre personalizado son opcionales</b>\n\nEjemplo de calidad: audio, 144, 240, 360, 480, 720, 1080, 2160."
        msg += "\n\nSi desea utilizar un nombre de archivo personalizado, ingréselo después |"
        msg += f"\n\nEjemplo:\n<code>/{BotCommands.WatchCommand} https://youtu.be/Pk_TthHfLeE 720 |Slam</code>\n\n"
        msg += "Este archivo se descargará en calidad 720p y su nombre será <b>Slam</b>"
        sendMessage(msg, bot, update)
        return
    
    try:
      if "|" in mssg:
        mssg = mssg.split("|")
        qual = mssg[0].split(" ")[2]
        if qual == "":
          raise IndexError
      else:
        qual = message_args[2]
      if qual != "audio":
        qual = f'bestvideo[height<={qual}]+bestaudio/best[height<={qual}]'
    except IndexError:
      qual = "bestvideo+bestaudio/best"
    
    try:
      name = name_args[1]
    except IndexError:
      name = ""
    
    pswd = ""
    listener = MirrorListener(bot, update, pswd, isTar)
    ydl = YoutubeDLHelper(listener)
    threading.Thread(target=ydl.add_download,args=(link, f'{DOWNLOAD_DIR}{listener.uid}', qual, name)).start()
    sendStatusMessage(update, bot)


def watchTar(update, context):
    _watch(context.bot, update, True)


def watch(update, context):
    _watch(context.bot, update)


mirror_handler = CommandHandler(BotCommands.WatchCommand, watch,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
tar_mirror_handler = CommandHandler(BotCommands.TarWatchCommand, watchTar,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)


dispatcher.add_handler(mirror_handler)
dispatcher.add_handler(tar_mirror_handler)
