#!/usr/bin/env python

import time
import logging
import random
import traceback
import html
import json

from telegram.ext import MessageHandler, CommandHandler, filters, Application
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode

from constants import bhagwan_naam

__author__ = "Rajas Rasam"
__credits__ = ["Rajas Rasam"]

__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Rajas Rasam"
__email__ = "rasamrajas@gmail.com"
__status__ = "Revision 8"

# Enable logging
logging.basicConfig(
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logging.info("Running Sticky Bot")

logger = logging.getLogger(__name__)

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)

# logger = logging.getLogger(__name__)

TOKEN = "6156340191:AAEgn6SZnKjFw64UTKQxfkhDauWpsE3djLk"
consumer_key = "fCMsvvmBzVmHDstVlFO5ozBhp"
consumer_secret = "lKrRBEiFLYgZsys1qM5tV0Iibz27cov0p88iHQArfeBejS4N49"
access_token = "1317099564571131906-IVgyp1pk4erRXXXY31GtECWmeDtDne"
access_token_secret = "VW8LQoWjwLHQ4KMVagQ56e4lrFe6fv3o6WJkQGgYPIHcz"
channel_id = "-1001120732795,-1001229637524"
group_id = "-1001305107479,-1001450746964"
access_id = "700426863,1685344499"

reply = """No unlawful discussions.
No incitement to violence.
No spam, no channel ads.
Respect others, be polite.
<code>
</code><b><i><u>We never contact you via DM: Block &amp; report such spammers.</u></i></b>"""

media_grp_id = []

keyboard = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton("Linktree", url="https://linktr.ee/AngrySaffron"),
        InlineKeyboardButton("Bharat Ke Veer",
                             url="https://bharatkeveer.gov.in/")
    ],
     [
         InlineKeyboardButton(
             "Press to Donate",
             url="https://tools.apgy.in/upi/Angry+Saffron/AngrySaffron@ybl/"),
         InlineKeyboardButton("Press to Boost",
                              url="https://t.me/angrysaffron?boost")
     ]])


# /Start Command
async def start(update, context):
    chat_id = update.message.chat.id
    bot = context.bot

    await bot.send_message(
        chat_id=chat_id,
        text=
        "राम राम\nThis bot is owned by @angrysaffron for sticky message purpose. Made by @Yuyutsu101."
    )


# This feature doesn't work without a db and I removed it from 0.1.0 as I don't know what server the owner will use and will my code with a DB run on it. I might do it in future depending on the undertanding of the server.
async def change_sticky_message(update, context):
    print(update)
    bot = context.bot
    message = update.message
    chat_id = message.chat.id

    if str(chat_id) in access_id:
        if message.reply_to_message:

            await bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=message.message_id,
                text='Successfully Saved! Example posted below.')

            await bot.send_message(chat_id=chat_id,
                                   reply_to_message_id=message.message_id,
                                   text=reply,
                                   reply_markup=keyboard,
                                   disable_web_page_preview=True,
                                   disable_notification=True,
                                   parse_mode=ParseMode.HTML)

        else:
            await bot.send_message(
                chat_id=chat_id,
                reply_to_message_id=message.message_id,
                text='Reply to the message you want to save')

    else:
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text=
            "Only Admins has access to use this command. Ask AngrySaffron owner to give access."
        )


async def channelpost(update, context):
    print(update)
    bot = context.bot
    message = update.message
    chat_id = message.chat.id
    from_chat = message.from_user
    from_chat_id = from_chat.id

    global media_grp_id

    if from_chat_id == 777000:
        sender = message.sender_chat
        sender_id = sender.id

        if str(sender_id) in channel_id:
            naam = random.choice(bhagwan_naam)

            try:
                var_media_group_id = message.media_group_id

                if bool(var_media_group_id):

                    if var_media_group_id not in media_grp_id:
                        await bot.send_message(
                            chat_id=chat_id,
                            reply_to_message_id=message.message_id,
                            text=f'{naam}\n\n{reply}',
                            disable_web_page_preview=True,
                            disable_notification=True,
                            reply_markup=keyboard,
                            parse_mode=ParseMode.HTML)

                        media_grp_id = media_grp_id + [var_media_group_id]
                else:
                    await bot.send_message(
                        chat_id=chat_id,
                        reply_to_message_id=message.message_id,
                        text=f'{naam}\n\n{reply}',
                        disable_web_page_preview=True,
                        disable_notification=True,
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML)
            except AttributeError:
                await bot.send_message(chat_id=chat_id,
                                       reply_to_message_id=message.message_id,
                                       text=f'{naam}\n\n{reply}',
                                       disable_web_page_preview=True,
                                       disable_notification=True,
                                       reply_markup=keyboard,
                                       parse_mode=ParseMode.HTML)


async def ping(update, context):
    bot = context.bot
    start = time.time()
    end = time.time()
    await bot.send_message(chat_id=update.message.chat.id,
                           text=f"Pong\n{end - start}")


async def error(update, context) -> None:
    bot = context.bot
    message = update.message
    chat_id = message.chat.id
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error,
                                         context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update,
                                                Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>")

    # Finally, send the message
    await context.bot.send_message(chat_id=700426863,
                                   text=message,
                                   parse_mode=ParseMode.HTML)


def main():
    dispatcher = Application.builder().token(TOKEN).build()
    # updater = Updater(TOKEN, use_context=True)
    # bot = updater.bot
    # dispatcher = updater.dispatcher
    # job = dispatcher.job_queue  # To queue jobs

    # Replies when you send a text message
    start_commandhandler = CommandHandler(["start", "help"],
                                          start,
                                          filters=filters.ChatType.PRIVATE)
    ping_commandhandler = CommandHandler("ping",
                                         ping,
                                         filters=filters.ChatType.PRIVATE)
    change_commandhandler = CommandHandler(["change", "save"],
                                           change_sticky_message,
                                           filters=filters.ChatType.PRIVATE)
    channelpost_messagehandler = MessageHandler(filters.ALL, channelpost)
    # example_func_messagehandler = MessageHandler(Filters.text, example_func)

    # Dispatchers
    dispatcher.add_handler(start_commandhandler)
    dispatcher.add_handler(change_commandhandler)
    dispatcher.add_handler(ping_commandhandler)
    dispatcher.add_handler(channelpost_messagehandler)
    # dispatcher.add_handler(example_func_messagehandler)

    dispatcher.add_error_handler(error)

    # Ctrl + C to stop
    dispatcher.run_polling(allowed_updates=Update.ALL_TYPES)
    # updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
