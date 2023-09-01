from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

from data_fetcher import fetch_data


waiting_for_inputs = []


main_menu_text = "Welcome, {username}!\n\n" \
                 "I'm <b>Nym Monitoring Bot</b>. Here you can monitor the transparency of any mix node " \
                 "(given the Mix ID): its status (active or not), uptime, total delegation & much more.\n\n" \
                 "Choose an option from the menu below."


main_menu_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Mixnode Info🧐",
            callback_data="mixnode_info"
        )
    ],
    [
        InlineKeyboardButton(
            text="Social handles📰",
            callback_data="social"
        )
    ]
])


social_text = "You can join official communities in <b>Discord</b> & <b>Telegram</b>, " \
              "also, don't forget to visit the website " \
              "for more info on Nym's solutions to privacy infrastructure problems!🔥✨"


social_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Discord👾",
            url="https://discord.gg/nym"
        )
    ],
    [
        InlineKeyboardButton(
            text="Official website🌍",
            url="https://nymtech.net/"
        )
    ],
    [
        InlineKeyboardButton(
            text="Telegram✈️",
            url="https://t.me/nymchan"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔙Back🔙",
            callback_data="main_menu"
        )
    ]
])


mix_node_text = "Mix ID: <b>{mix_id}</b>\n\n" \
                "Identity Key: <b>{identity}</b>\n" \
                "Owner's wallet: <a href=\"https://mixnet.explorers.guru/account/{wallet}\">{wallet}</a>\n\n" \
                "Mixnode went online on <b>{earliest_entry}</b>\n" \
                "Average uptime since then: <b><u>{all_time_uptime}</u></b>\n\n" \
                "• recent uptime (today): <b>{recent_uptime}</b>%\n" \
                "• last hour uptime: <b>{last_hour_uptime}</b>%\n" \
                "• last day uptime: <b>{last_day_uptime}</b>%"

mix_node_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Try another Mix ID🔄",
            callback_data="try_again"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔙Back🔙",
            callback_data="main_menu"
        )
    ]
])


def button_handler(update: Update, context: CallbackContext):
    data = update.callback_query.data
    username = update.callback_query.from_user.username

    if data == "main_menu":
        update.callback_query.message.edit_text(
            main_menu_text.replace("{username}", f"@{username}"),
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_markup
        )
    elif data == "social":
        update.callback_query.message.edit_text(
            social_text,
            parse_mode=ParseMode.HTML,
            reply_markup=social_markup
        )
    elif data == "mixnode_info":
        if username not in waiting_for_inputs:
            waiting_for_inputs.append(username)

            context.bot.send_message(
                update.callback_query.from_user.id,
                "📝Send me the <b>Mix ID</b> of a mixnode to retrieve the information.",
                parse_mode=ParseMode.HTML
            )
        else:
            context.bot.send_message(
                update.callback_query.from_user.id,
                "🧐You have already chosen the option to get the mixnode info – send me the <b>Mix ID</b>.",
                parse_mode=ParseMode.HTML
            )
    elif data == "try_again":
        if username not in waiting_for_inputs:
            waiting_for_inputs.append(username)

            context.bot.send_message(
                update.callback_query.from_user.id,
                "📝Send me the <b>Mix ID</b> of a mixnode to retrieve the information.",
                parse_mode=ParseMode.HTML
            )
        else:
            context.bot.send_message(
                update.callback_query.from_user.id,
                "🧐You have already chosen the option to get the mixnode info – send me the <b>Mix ID</b>.",
                parse_mode=ParseMode.HTML
            )

        context.bot.delete_message(
            update.callback_query.from_user.id,
            update.callback_query.message.message_id
        )


def text_handler(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    text = update.message.text

    if username not in waiting_for_inputs:
        context.bot.send_message(
            update.message.from_user.id,
            "🤨Unfortunately, I don't understand text inputs aside from when you need to get mixnode info.\n\n"
            "Choose an option \"Mixnode Info🧐\" from the main menu to proceed.",
            parse_mode=ParseMode.HTML
        )
    else:
        waiting_for_inputs.remove(username)
        if not text.isnumeric():
            context.bot.send_message(
                update.message.from_user.id,
                f"⛔️You have entered <b>invalid</b> Mix ID.\n\n"
                "Try again.",
                parse_mode=ParseMode.HTML
            )

            context.bot.delete_message(
                update.message.from_user.id,
                update.message.message_id
            )

            return

        mix_id = int(text)
        if mix_id > 0:
            result = fetch_data(mix_id)

            if len(result) == 0:
                context.bot.send_message(
                    update.message.from_user.id,
                    f"🤒The data for Mix ID {mix_id} is <b>unavailable</b>.\n\n"
                    "Are you sure you entered a <b>valid</b> ID? Try again.",
                    parse_mode=ParseMode.HTML
                )
            else:
                result_text = mix_node_text.\
                    replace("{mix_id}", str(result["mix_id"])).\
                    replace("{identity}", result["identity"]).\
                    replace("{wallet}", result["wallet"]).\
                    replace("{earliest_entry}", result["earliest_entry"]).\
                    replace("{all_time_uptime}", str(result["all_time_uptime"])).\
                    replace("{recent_uptime}", str(result["recent_uptime"])).\
                    replace("{last_hour_uptime}", str(result["last_hour_uptime"])).\
                    replace("{last_day_uptime}", str(result["last_day_uptime"]))

                context.bot.send_message(
                    update.message.from_user.id,
                    result_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=mix_node_markup,
                    disable_web_page_preview=True
                )
        else:
            context.bot.send_message(
                update.message.from_user.id,
                f"⛔️You may have entered <b>invalid</b> Mix ID.\n\n"
                "Try again."
            )

    context.bot.delete_message(
        update.message.from_user.id,
        update.message.message_id
    )


def start_handler(update: Update, context: CallbackContext):
    context.bot.send_message(
        update.message.from_user.id,
        main_menu_text.replace("{username}", f"@{update.message.from_user.username}"),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_markup
    )

    context.bot.delete_message(
        update.message.chat_id,
        update.message.message_id
    )


def main():
    updater = Updater(
        token="<YOUR_TOKEN_HERE>"
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
