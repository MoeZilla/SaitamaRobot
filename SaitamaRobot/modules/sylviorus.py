# create module by moezilla 
# join @sylviorus_support

import os
from sylviorus import SYL
import json
import re
import os
import html
import requests
from telegram.ext.filters import Filters
from telegram.parsemode import ParseMode

import Moebot.modules.sql.syl_sql as sql

from time import sleep
from telegram import ParseMode
from telegram import (CallbackQuery, Chat, MessageEntity, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ParseMode, Update, Bot, User)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

from Moebot.modules.helper_funcs.filters import CustomFilters
from Moebot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from Moebot import dispatcher, updater, SUPPORT_CHAT
from Moebot.modules.log_channel import gloggable

xsyl = SYL()
 
@user_admin_no_reply
@gloggable
def sylrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    if match := re.match(r"rm_syl\((.+?)\)", query.data):
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        if is_syl := sql.rem_syl(chat.id):
            is_syl = sql.rem_syl(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"SYL_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Syl disable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def syladd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    if match := re.match(r"add_syl\((.+?)\)", query.data):
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        if is_syl := sql.set_syl(chat.id):
            is_syl = sql.set_syl(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"SYL_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Syl Enable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def bluemoon(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data="add_syl({})")],
       [
        InlineKeyboardButton(
            text="Disable",
            callback_data="rm_syl({})")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def bluemoon_callback(update: Update, context: CallbackContext, should_message=True):
    message = update.effective_message
    chat_id = update.effective_chat.id
    user = update.effective_user

    if is_syl := sql.is_syl(chat_id):
        return
    try:
        x = xsyl.check(int(user.id))
    except:
        x = None

    if x:
        update.effective_chat.ban_member(x.user)
        update.effective_chat.unban_member(x.user)
        if should_message:
            update.effective_message.reply_text(
                f"<b>Alert</b>: This User Is Blacklisted\n"
                f"<code>*bans them from here*</code>.\n"
                f"<b>Appeal chat</b>: @Sylviorus_support\n"
                f"<b>User ID</b>: <code>{x.user}</code>\n"
                f"<b>Enforcer</b>: <code>{x.enforcer}</code>\n"
                f"<b>Reason</b>: <code>{x.reason}</code>",
                parse_mode=ParseMode.HTML,
            )
        return


BLUEMOON_HANDLER = CommandHandler("syl", bluemoon, run_async=True)
ADD_SYL_HANDLER = CallbackQueryHandler(syladd, pattern=r"add_syl", run_async=True)
RM_SYL_HANDLER = CallbackQueryHandler(sylrm, pattern=r"rm_syl", run_async=True)
BLUEMOON_HANDLERK = MessageHandler(filters=Filters.all & Filters.group, callback=bluemoon_callback)

dispatcher.add_handler(ADD_SYL_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLER)
dispatcher.add_handler(RM_SYL_HANDLER)
dispatcher.add_handler(BLUEMOON_HANDLERK, group=102)
