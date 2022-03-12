# Bot for service market

 - project in beta version.

[![Python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)

![screenshot1](search_services_bot/images/Screenshot%20from%202022-03-06%2016-35-34.png)  

## Description
By using this bot, user of service market can create advertisement or watch them. User can be:
1) Master - can create advertising services or watch advertising services craating by your self
2) Customer - can watch all the advertisements of all masters

All the users have a customer role, for the master role you need to be entered to DB.
Administrator can create/correct advertisement, list masters by using django admin panel.

## How to install
 - clone project

```shell
git clone https://github.com/toshiharu13/search_services_bot.git
```
 - Installing requirements.txt
```shell
pip install -r requirements.txt
```
 - Create .env file and fill it with variables:
 
```dotenv
TG_BOT_TOKEN = 'token of telegram bot'
```
## How to run
to run bot:
```shell
python3 manage.py tg_bot
```
to run django service:
```shell
python3 manage.py
```

## Goal of project
program was created for education purpose for [Devman](https://dvmn.org).
