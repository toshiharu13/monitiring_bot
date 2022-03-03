import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from environs import Env
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from telegram.utils.request import Request


CUSTOMER, = range(1)


def start(update, context):
    update.message.reply_text('Превед! я ботяшка помогашка!')


def customer_view():
    ...


def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    #logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


class Command(BaseCommand):
    help = "search_services_bot"

    def handle(self, *args, **options):
        env = Env()
        env.read_env()
        TG_TOKEN = env.str("TG_TOKEN")
        bot = Bot(
            token=TG_TOKEN,
            base_url=getattr(settings, "PROXY_URL", None),
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        conv_handler = ConversationHandler(
                entry_points=[CommandHandler("start", start)],
                states={CUSTOMER: [CallbackQueryHandler(
                    customer_view,
                    pattern='\S')
                    ]},
                fallbacks=[CommandHandler("end", cancel)],
            )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()