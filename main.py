
'''
    Telegram bot to remember my friends' birthdays :)
'''

from bot import Bot

# Token provided by telegram
TOKEN = 'xxxxxxxxxxxx'

def main():
    bot = Bot(TOKEN) # creates bot
    bot.add_commands() # add commands
    bot.turn_on() 
    bot.turn_off()

if __name__ == '__main__':
    main()
