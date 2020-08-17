import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Contact
from emoji import emojize
from bs4 import BeautifulSoup

# related to errors and exceptions
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

'''
    This class defines the bot behavior, and its answer to each command.
'''
class GenericBot:
    def __init__(self,token):
        self.__token = token
        self.__updater = Updater(token=self.__token , use_context=True)
        self.__dispatcher = self.__updater.dispatcher

    '''
        Behavior to the /help command.
    '''
    def __helpp(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text= self.__get_txt("text/help.txt"))  # sends a .txt 

    '''
        /star command initializes the bot
    '''
    def __start(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-vindo ao bot de lembretes de aniversários do PET! :)")
        self.__helpp(update, context)
        self.__teclado(update, context)


    '''
        When the bot doesn't know the command.
    '''
    def __unknown(self,update,context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Comando inexistente. Por favor, tente novamente.")

    '''
        auxiliar function to read .txt files
    '''
    def __get_txt(self,file_name):
        file = open(file_name, "r")
        message = file.read()
        file.close()
        return message


    '''
        Cria o handler que lida com cada comando, ou seja, liga um tipo de mensagem específica do bot com as fuções de comportamento dele
    '''
    def add_commands(self):
        self.__dispatcher.add_handler(CommandHandler("start",self.__start))
        self.__dispatcher.add_handler(CommandHandler("estado",self.__estado))
        self.__dispatcher.add_handler(CommandHandler("emergencia",self.__emergencia))
        self.__dispatcher.add_handler(CommandHandler("sintomas",self.__sintomas))
        self.__dispatcher.add_handler(CommandHandler("help",self.__helpp))
        self.__dispatcher.add_handler(CommandHandler("news",self.__news))
        self.__dispatcher.add_handler(CommandHandler("local",self.__local))
        self.__dispatcher.add_handler(CommandHandler("ministro",self.__ministro))
        unknown_handler = MessageHandler(filters=Filters.text, callback=self.__handle_message)
        unknown_command = MessageHandler(filters=Filters.command,callback=self.__unknown)
        self.__dispatcher.add_handler(unknown_handler)
        self.__dispatcher.add_handler(unknown_command)


    
    def turn_on(self):
        self.__updater.start_polling()
        logging.info("### It's alive! ###")

    
    def turn_off(self):
        self.__updater.idle()
        logging.info("### It's dead! ###")
