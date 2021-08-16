# Implement By https://github.com/jusidama18
# Based on this https://github.com/DevsExpo/FridayUserbot/blob/master/plugins/heroku_helpers.py

from pyrogram import filters, types, emoji
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import app, OWNER_ID, bot
from bot.helper import get_text, check_heroku
from bot import *

# Add Variable

@app.on_message(filters.command(['setvar', f'setvar@{bot.username}']) & filters.user(OWNER_ID))
@check_heroku
async def set_varr(client, message, app_):
    msg_ = await message.reply_text("`Please Wait!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg_.edit("`Aquí está la sintaxis de uso: /setvar KEY VALUE`", parse_mode="markdown")
        return
    if not " " in _var:
        await msg_.edit("`Se necesita una variable VALUE !`", parse_mode="markdown")
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg_.edit("`Aquí está la sintaxis de uso: /setvar KEY VALUE`", parse_mode="markdown")
        return
    _varname, _varvalue = var_
    await msg_.edit(
        f"`Variable {_varname} Agregado con valor {_varvalue}!`" \
        f"\nSu aplicación Heroku se reiniciará. Ser paciente."
    )
    heroku_var[_varname] = _varvalue

# Delete Variable
        
@app.on_message(filters.command(['delvar', f'delvar@{bot.username}']) & filters.user(OWNER_ID))
@check_heroku
async def del_varr(client, message, app_):
    msg_ = await message.reply_text("`Espere por favor!`", parse_mode="markdown")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg_.edit("`Dar nombre de var como entrada!`", parse_mode="markdown")
        return
    if not _var in heroku_var:
        await msg_.edit("`Este var no existe!`", parse_mode="markdown")
        return
    await msg_.edit(
        f"`Eliminado exitosamente {_var} Var!`" \
        f"\nSu aplicación Heroku se reiniciará. Ser paciente.",
        parse_mode="markdown")
    del heroku_var[_var]

@app.on_message(filters.command(['reboot', f'reboot@{bot.username}']) & filters.user(OWNER_ID))
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_text("[HEROKU] - Reiniciando")
    hap.restart()

# CONFIG LIST #

__header__='📕 **Página** **{}**\n\n'

@app.on_message(filters.command([BotCommands.ConfigMenuCommand, f'{BotCommands.ConfigMenuCommand}@{bot.username}']) & filters.user(OWNER_ID))
async def config_menu(_, message):
    await message.reply(
        f"**Hello {message.from_user.mention}**,\n\n**Si desea agregar o establecer una variable en Heroku, use** `/setvar`\n\n**Si desea eliminar Variable en Heroku use `/delvar`**\n\n**ADVERTENCIA! Muy recomendado para hacer este comando en privado ya que contiene información del Bot.**\n\n**Aquí está esta es la configuración actual de Slam-MirrorBot**",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'), types.InlineKeyboardButton(f"CONFIGURAR BOT", callback_data='docs_1')]]
        )
    )

@app.on_callback_query(filters.regex('^docs_') & filters.user(OWNER_ID))
async def config_button(_, query):
    data = query.data.split('_')[1]
    if data == '1':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de Telegram ]**\n\n**BOT_TOKEN:** `{BOT_TOKEN}`\n\n**TELEGRAM_API:** `{TELEGRAM_API}`\n\n**TELEGRAM_HASH:** `{TELEGRAM_HASH}`\n\n**TELEGRAPH_TOKEN:** `{telegraph_token}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_10'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_2')
                    ]
                ]
            )
        )
    elif data == '2':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de índice y unidad ]**\n\n**GDRIVE_FOLDER_ID:** `{parent_id}`\n\n**IS_TEAM_DRIVE:** `{IS_TEAM_DRIVE}`\n\n**USE_SERVICE_ACCOUNTS:** `{USE_SERVICE_ACCOUNTS}`\n\n**INDEX_URL:** `{INDEX_URL}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_1'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_3')
                    ]
                ]
            )
        )
    elif data == '3':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de Mega y Uptobox ]**\n\n**MEGA_API_KEY:** `{MEGA_API_KEY}`\n\n**MEGA_EMAIL_ID:** `{MEGA_EMAIL_ID}`\n\n**MEGA_PASSWORD:** `{MEGA_PASSWORD}`\n\n**UPTOBOX_TOKEN:** `{UPTOBOX_TOKEN}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_2'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_4')
                    ]
                ]
            )
        )
    elif data == '4':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Detener y bloquear la configuración ]**\n\n**STOP_DUPLICATE:** `{STOP_DUPLICATE}`\n\n**BLOCK_MEGA_FOLDER:** `{BLOCK_MEGA_FOLDER}`\n\n**BLOCK_MEGA_LINKS:** `{BLOCK_MEGA_LINKS}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_3'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_5')
                    ]
                ]
            )
        )
    elif data == '5':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de tamaño límite ]**\n\n**TORRENT_DIRECT_LIMIT:** `{TORRENT_DIRECT_LIMIT}`\n\n**TAR_UNZIP_LIMIT:** `{TAR_UNZIP_LIMIT}`\n\n**CLONE_LIMIT:** `{CLONE_LIMIT}`\n\n**MEGA_LIMIT:** `{MEGA_LIMIT}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_4'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_6')
                    ]
                ]
            )
        )
    elif data == '6':
        user = sudo = ''
        user += '\n'.join(str(id) for id in AUTHORIZED_CHATS)
        sudo += '\n'.join(str(id) for id in SUDO_USERS)
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de ID de usuario ]**\n\n**OWNER_ID:** `{OWNER_ID}`\n\n**AUTHORIZED_CHATS:**\n`{user}`\n\n**SUDO_USERS:**\n`{sudo}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_5'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_7')
                    ]
                ]
            )
        )
    elif data == '7':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración del botón ]**\n\n**BUTTON_FOUR_NAME:** `{BUTTON_FOUR_NAME}`\n\n**BUTTON_FOUR_URL:** `{BUTTON_FOUR_URL}`\n\n**BUTTON_FIVE_NAME:** `{BUTTON_FIVE_NAME}`\n\n**BUTTON_FIVE_URL:** `{BUTTON_FIVE_URL}`\n\n**BUTTON_SIX_NAME:** `{BUTTON_SIX_NAME}`\n\n**BUTTON_SIX_URL:** `{BUTTON_SIX_URL}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_6'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_8')
                    ]
                ]
            )
        )
    elif data == '8':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Configuración de Heroku ]**\n\n**HEROKU_API_KEY:** `{HEROKU_API_KEY}`\n\n**HEROKU_APP_NAME:** `{HEROKU_APP_NAME}`\n\n**[ Shortener Config ]**\n\n**SHORTENER:** `{SHORTENER}`\n\n**SHORTENER_API:** `{SHORTENER_API}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_7'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_9')
                    ]
                ]
            )
        )
    elif data == '9':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ Otros Config ]**\n\n**VIEW_LINK:** `{VIEW_LINK}`\n\n**STATUS_LIMIT:** `{STATUS_LIMIT}`\n\n**DOWNLOAD_STATUS_UPDATE_INTERVAL:** `{DOWNLOAD_STATUS_UPDATE_INTERVAL}`\n\n**IGNORE_PENDING_REQUESTS:** `{IGNORE_PENDING_REQUESTS}`\n\n**AUTO_DELETE_MESSAGE_DURATION:** `{AUTO_DELETE_MESSAGE_DURATION}`\n\n**DOWNLOAD_DIR:** `{DOWNLOAD_DIR}`\n\n**DATABASE_URL:** `{DB_URI}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_8'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_10')
                    ]
                ]
            )
        )
    elif data == '10':
        return await query.message.edit(
            __header__.format(data)
            + f"**[ qBittorrent Config ]**\n\n**IS_VPS:** `{IS_VPS}`\n\n**SERVER_PORT:** `{SERVER_PORT}`\n\n**BASE_URL_OF_BOT:** `{BASE_URL}`\n\n**[ Updater Config ]**\n\n**UPSTREAM_REPO:** `{UPSTREAM_REPO}`\n\n**UPSTREAM_BRANCH:** `{UPSTREAM_BRANCH}`",
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(f"{emoji.LEFT_ARROW}", callback_data='docs_9'),
                        types.InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data='docs_end'),
                        types.InlineKeyboardButton(f"{emoji.RIGHT_ARROW}", callback_data='docs_1')
                    ]
                ]
            )
        )
    elif data == 'end':
        return await query.message.delete()
