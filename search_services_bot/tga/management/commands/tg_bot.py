import textwrap

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from environs import Env
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)
from tga.models import Client, Service, TypeOfService

CUSTOMER, SERVICETYPE, REGTIME, REGPRICE, REGTEXT, SAVESERVICE, MASTERVIEW= range(7)


def start(update, context):
    chat_id = update.effective_chat.id
    keyboard = []
    message_text = textwrap.dedent = (f'''\
    Твой ID - {chat_id}
    
    Превед! я ботяшка  сервисы продавашка! 
    если вдруг надоело, жахни /end 
    и я пойду разберать дальше свои шуты''')

    master_or_not = Client.objects.all().filter(id_telegtam__contains=chat_id)
    if master_or_not:
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
    services = Service.objects.filter(
        type_of_service__type_of_service__contains=type_of_service)

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
    bot = context.bot
    chat_id = update.message.chat.id
    text = f'''\
    Введена цена - {new_service_price} рублей
    Введите описание вашей услуги
'''
    bot.send_message(chat_id=chat_id, text=text)

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

    new_service = save_service_to_bd(chat_id)

    text = f'''\
    Зарегестрирована услуга № {new_service.pk}
    
    Тип сервиса: {new_service.type_of_service}
    Время работ в днях: {new_service.time_to_work}
    Цена услугив рублях: {new_service.price}
    Описание услуги: {new_service.description}
    Имя мастера: {new_service.master}
    Номер телефона: {new_service.master.phone_number}
    '''
    bot.send_message(chat_id=chat_id, text=text)


def save_service_to_bd(chat_id):
    global new_service_type
    global new_service_time
    global new_service_price
    global new_service_text

    type_of_service_fg = get_object_or_404(
        TypeOfService, type_of_service=new_service_type)
    master_fg = get_object_or_404(Client, id_telegtam=chat_id)

    new_service = Service.objects.get_or_create(
        type_of_service=type_of_service_fg,
        time_to_work=new_service_time,
        price=new_service_price,
        description=new_service_text,
        master=master_fg)

    return new_service[0]


def get_master_view(update, context):
    keyboard = []
    bot = context.bot
    chat_id = update.callback_query.from_user.id
    text_type = f'''
        Выбирете операцию роли мастер
        '''

    keyboard.append([InlineKeyboardButton(
        text='Создание объявления', callback_data='newservice')])
    keyboard.append([InlineKeyboardButton(
        text='Просмотр объявлений', callback_data='oldservice')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text=text_type,
        reply_markup=reply_markup, )

    return MASTERVIEW


def get_masters_services(update, context):
    bot = context.bot
    chat_id = update.callback_query.from_user.id
    masters_services = Service.objects.all().filter(master__id_telegtam=chat_id)

    for service in masters_services:
        text = f'''\
            Зарегестрирована услуга № {service.pk}

            Тип сервиса: {service.type_of_service}
            Время работ в днях: {service.time_to_work}
            Цена услугив рублях: {service.price}
            Описание услуги: {service.description}
            Имя мастера: {service.master}
            Номер телефона: {service.master.phone_number}
            '''
        bot.send_message(chat_id=chat_id, text=text)


def end(update, context):
    message_text = f'''Заходи ещё! пойду разбиру чего'
    Будет скучно - пиши.'''

    update.message.reply_text(message_text)

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
                        CallbackQueryHandler(
                            customer_view, pattern='^'+'customer'+'$'),
                        CallbackQueryHandler(
                            get_master_view, pattern='^master$'),
                    ],
                    MASTERVIEW: [
                        CallbackQueryHandler(reg_service_type,
                                             pattern='^newservice$'),
                        CallbackQueryHandler(get_masters_services,
                                             pattern='^oldservice$'),
                    ],
                    SERVICETYPE: [
                        CallbackQueryHandler(
                            get_one_type_services, pattern='\S',)],
                    REGTIME: [
                        CallbackQueryHandler(reg_service_time, pattern='\S',)],
                    REGPRICE: [
                        MessageHandler(
                            Filters.text & ~Filters.command, ger_service_price)],
                    REGTEXT: [
                        MessageHandler(
                            Filters.text & ~Filters.command, reg_service_text)],
                    SAVESERVICE: [
                        MessageHandler(
                            Filters.text & ~Filters.command, creating_service)],
                },
                fallbacks=[CommandHandler("end", end)],
            )

        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
