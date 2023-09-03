import logging

from telegram import MenuButtonCommands, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot.constants.buttons import HELP_BUTTON, MAIN_BUTTONS
from bot.constants.commands import COMMANDS
from bot.constants.messages import (MENU_MESSAGE, START_MESSAGE,
                                    TEXT_ANSWER_MESSAGE)
from bot.constants.logging_messages import START_BOT_LOG
from bot.utils import get_user_info


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start or /help is issued."""
    if update.message.text == '/start':
        logging.info(START_BOT_LOG.format(get_user_info(update)))
        bot_commands = await context.bot.get_my_commands()
        if not bot_commands:
            await context.bot.set_my_commands(commands=COMMANDS)
            await context.bot.set_chat_menu_button(
                menu_button=MenuButtonCommands()
            )

    await update.message.reply_html(
        START_MESSAGE.format(update.effective_user.mention_html()),
        reply_markup=MAIN_BUTTONS
    )


async def show_menu(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Shows the bot menu to the user."""
    await update.message.reply_text(
        MENU_MESSAGE,
        reply_markup=MAIN_BUTTONS
    )


async def text_answer(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Replies to the user with a normal message."""
    await update.message.delete()
    await update.message.reply_text(
        TEXT_ANSWER_MESSAGE,
        reply_markup=MAIN_BUTTONS
    )


start_handler = MessageHandler(
    filters.Regex(HELP_BUTTON)
    | filters.Regex("/start")
    | filters.Regex("/help"),
    start
)
menu_handler = CommandHandler('menu', show_menu)
text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, text_answer)
