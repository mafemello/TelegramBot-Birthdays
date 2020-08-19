import logging
import requests
import json
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Contact
from telegram.utils.helpers import to_float_timestamp  
from emoji import emojize
from bs4 import BeautifulSoup
from happy_birthday import happyBirthday
from next_birthday import nextBirthday
from birthday_year import BirthdayYear
import schedule
import time


# related to errors and exceptions
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

'''
    This class defines the bot behavior, and its answer to each command.
'''
class Bot:
    def __init__(self,token):
        self.__token = token
        self.__updater = Updater(token=self.__token , use_context=True)
        self.__dispatcher = self.__updater.dispatcher

    '''
        Behavior to the /help command.
    '''
    def __helpp(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text= self.__get_txt("help.txt"))  # sends a .txt 

    '''
        /start command initializes the bot
    '''
    def __start(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-vindo ao bot de lembretes de aniversários do PET! :)")
        self.__helpp(update, context)
        self.__keybord(update, context)


    '''
        When the bot doesn't know the command.
    '''
    def __unknown(self,update,context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Comando inexistente. Por favor, tente novamente.")


    '''
        Shows next birthday ==> done 
        /proximo
    '''
    def _next_birthday (self,update,context):
        nb = nextBirthday(context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text= nb.get_message())

    '''
        Shows all birthdays in a year ==> done
        /todos
    '''
    def _all_birthdays (self, update, context):
        by = BirthdayYear (context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text= by.get_message())

    '''
        Sends a happy birthday message!
        This function must run daily so it can check if it is the day.
        /hoje
    '''
    def happy_birthday (self, update, context):
        hb = happyBirthday (context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text= hb.get_message())        
        
    schedule.every().day.at("10:30").do(happy_birthday)

    '''
        Cute keybord layout
    '''
    def __keybord(self,update, context):
        custom_keyboard =   [
                                [emojize(":arrow_right: Próximo", use_aliases=True) ,
                                emojize(":calendar: Todos", use_aliases=True)],
                                [emojize(":birthday: Hoje", use_aliases=True)],
                                [emojize(":information_source: Ajuda", use_aliases=True)]
                            ]
        kbrd = ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=emojize("#PETComp :computer:", use_aliases=True), reply_markup=kbrd)

    '''
        The keybord generates commands, this method conects the behavior
    '''
    def __handle_message(self,update, context):
        [emojize(":arrow_right: Proximo", use_aliases=True) ,
        emojize(":calendar: Todos", use_aliases=True)],
        [emojize(":birthday: Hoje", use_aliases=True),
        emojize(":information_source: Ajuda", use_aliases=True)]
        text = update.message.text
        if text == emojize(":arrow_right: Próximo", use_aliases=True):
            self._next_birthday(update, context)
        elif text == emojize(":calendar: Todos", use_aliases=True):
            self._all_birthdays(update, context)
        elif text == emojize(":birthday: Hoje", use_aliases=True):
            self.happy_birthday(update, context)
        elif text == emojize(":information_source: Ajuda", use_aliases=True):
            self.__helpp(update, context)
        else:
            self.__unknown(update, context)

    '''
        Handler connects the commands to its behavior
    '''
    def add_commands(self):
        self.__dispatcher.add_handler(CommandHandler("start",self.__start))
        self.__dispatcher.add_handler(CommandHandler("proximo",self._next_birthday))
        self.__dispatcher.add_handler(CommandHandler("todos",self._all_birthdays))
        self.__dispatcher.add_handler(CommandHandler("hoje",self.happy_birthday))
        self.__dispatcher.add_handler(CommandHandler("help",self.__helpp))
        unknown_handler = MessageHandler(filters=Filters.text, callback=self.__handle_message)
        unknown_command = MessageHandler(filters=Filters.command,callback=self.__unknown)
        self.__dispatcher.add_handler(unknown_handler)
        self.__dispatcher.add_handler(unknown_command)


    '''
        auxiliar function to read .txt files
    '''
    def __get_txt(self,file_name):
        file = open(file_name, "r")
        message = file.read()
        file.close()
        return message



    def turn_on(self):
        self.__updater.start_polling()
        logging.info("### It's alive! ###")

    
    def turn_off(self):
        self.__updater.idle()
        logging.info("### It's dead! ###")
