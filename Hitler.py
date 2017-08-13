from sopel.module import commands

players = []
ongoing = False

@commands('hello')
def hello(bot, trigger):
    bot.say("Hello!")


@commands('hitler')
def start(bot, trigger):
    bot.say("Someone has started a game of Secret Hitler! Type .join to join!")
    players.append(trigger.nick)
    bot.say(trigger.nick+" has joined up! Type .flee to leave with your tail tucked between your legs!")


@commands('join')
def join(bot, trigger):
    if trigger.nick not in players:
        players.append(trigger.nick)
        bot.say(trigger.nick+" has joined up!")
    else:
        bot.say("You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!")

@commands('flee')
def quit(bot, trigger):
    if ongoing is False:
        if trigger.nick in players:
            players.remove(trigger.nick)
            bot.say(trigger.nick+" has left the game. Coward.")
        else:
            bot.say("You're not signed up you dimwit!")
    else:
        bot.say("The game is still ongoing, you dimwit, you can't leave until Hilter is dead!")
