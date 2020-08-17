
'''
    Telegram bot to remember my friends' birthdays :)
'''

from generic_bot import GenericBot

# Token provided by telegram
TOKEN = 'XXXXXXXXXXXXXXXXXXXXX'

def main():
    bot = GenericBot(TOKEN) # creates bot
    bot.add_commands() # add commands
    bot.turn_on() 
    bot.turn_off()

if __name__ == '__main__':
    main()
