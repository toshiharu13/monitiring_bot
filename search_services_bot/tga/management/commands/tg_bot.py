import json
import textwrap

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from environs import Env
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

from telegram.utils.request import Request
from tga.models import TypeOfService, Service, Client


CUSTOMER, SERVICETYPE, REGTIME, REGPRICE, REGTEXT, SAVESERVICE= range(6)


def start(update, context):
    chat_id = update.effective_chat.id
    #print(update)
    keyboard = []
    message_text = textwrap.dedent = (f'''\
    Твой ID - {chat_id}
    
    Превед! я ботяшка  сервисы продавашка! 
    если вдруг надоело, жахни /end 
    и я пойду разберать дальше свои шуты''')

    master_or_not = Client.objects.all().filter(id_telegtam__contains=chat_id)
    if master_or_not:
        #print('yes my master!')
        keyboard.append([InlineKeyboardButton(
            text='master', callback_data='master')])

    update.message.reply_text(message_text)

    keyboard.append(
        [InlineKeyboardButton(text='customer', callback_data='customer'),]
    )


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("выберите роль", reply_markup=reply_markup,)
    return CUSTOMER


def customer_view(update, context):
    bot = context.bot
    keyboard = []
    all_types = TypeOfService.objects.all()

    for service_type in all_types:
        service_type = str(service_type)
        keyboard.append([InlineKeyboardButton(
            text=service_type, callback_data=str(service_type))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text='Выбирите услугу',
        reply_markup=reply_markup,)

    return SERVICETYPE


def get_one_type_services(update, context):
    bot = context.bot
    type_of_service = update.callback_query.data
    print(type_of_service)
    print(type(type_of_service))
    services = Service.objects.filter(type_of_service__type_of_service__contains=type_of_service)
    print(services)
    for service in services:
        text = f'''\
        Тип сервиса: {service.type_of_service}
        Время работ в днях: {service.time_to_work}
        Цена услугив рублях: {service.price}
        Описание услуги: {service.description}
        Имя мастера: {service.master}
        Номер телефона: {service.master.phone_number}
        '''
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text=text)


def reg_service_type(update, context):
    keyboard = []
    bot = context.bot
    chat_id = update.callback_query.from_user.id
    text_type = f'''
    Создание объявления,
    Введите тип услуги
    '''
    all_types = TypeOfService.objects.all()

    for service_type in all_types:
        service_type = str(service_type)
        keyboard.append([InlineKeyboardButton(
            text=service_type, callback_data=str(service_type))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text=text_type,
        reply_markup=reply_markup,)

    #print(update)
    return REGTIME


def reg_service_time(update, context):
    global new_service_type
    new_service_type = update.callback_query.data
    bot = context.bot
    chat_id = update.callback_query.from_user.id
    text = f'''\
     Выбран тип - {new_service_type}
     введите время работ в днях
     '''

    bot.send_message(chat_id=chat_id, text=text)

    return REGPRICE


def ger_service_price(update, context):
    global new_service_time
    new_service_time = update.message.text
    bot = context.bot
    #print(update.message.chat)
    chat_id = update.message.chat.id
    text = f'''\
    ВВедено время работ - {new_service_time} дней
    Введите цену услуги целыми числами
    '''

    bot.send_message(chat_id=chat_id, text=text)

    return REGTEXT


def reg_service_text(update, context):
    global new_service_price
    new_service_price = update.message.text
    #print(new_service_price)
    bot = context.bot
    chat_id = update.message.chat.id
    text = f'''\
    Введена цена - {new_service_price} рублей
    Введите описание вашей услуги
'''
    bot.send_message(chat_id=chat_id, text=text)
    #print(update)
    return SAVESERVICE


def creating_service(update, context):
    global new_service_text
    new_service_text = update.message.text
    chat_id = update.message.chat.id
    bot = context.bot
    text = f'''\
    Введен текст:
    {new_service_text}
    обработка данных...
'''
    bot.send_message(chat_id=chat_id, text=text)
    #print(new_service_text)


def save_service_to_bd():
    global new_service_type
    global new_service_time
    global new_service_price
    global new_service_text





def end(update, context):
    message_text = f'''Заходи ещё! пойду разбиру чего'
    Будет скучно - пиши.'''
    update.message.reply_text(message_text)
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
                states={
                    CUSTOMER: [
                        CallbackQueryHandler(customer_view, pattern='^'+'customer'+'$'),
                        CallbackQueryHandler(reg_service_type, pattern='^master$'),
                    ],
                    SERVICETYPE: [
                        CallbackQueryHandler(get_one_type_services, pattern='\S',)],
                    REGTIME: [
                        CallbackQueryHandler(reg_service_time, pattern='\S',)],
                    REGPRICE: [
                        MessageHandler(Filters.text & ~Filters.command, ger_service_price)],
                    REGTEXT: [
                        MessageHandler(Filters.text & ~Filters.command, reg_service_text)],
                    SAVESERVICE: [
                        MessageHandler(Filters.text & ~Filters.command, creating_service)],
                },
                fallbacks=[CommandHandler("end", end)],
            )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
