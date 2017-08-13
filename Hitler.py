from sopel.module import commands

players = []
global ongoing
ongoing = False
owner = 'VereorNox'
finished = 0



@commands('hello')
def hello(bot, trigger):
    bot.say("Hello!")


@commands('hitler')
def start(bot, trigger):
    bot.say("Someone has started a game of Secret Hitler! Type .join to join!")
    players.append(trigger.nick)
    bot.say(trigger.nick+" has joined up! Type .flee to leave with your tail tucked between your legs!")


@commands('join')
def joinGame(bot, trigger):
    if trigger.nick not in players:
        players.append(trigger.nick)
        bot.say(trigger.nick+" has joined up!")
    else:
        bot.say("You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!")


@commands('quit')
def stopGame(bot, trigger):
    if ongoing is False:
        if trigger.nick is players[0]:
            bot.say("The game was aborted by the creator "+trigger.nick)
        else:
            bot.say("You didn't start this game, you fool!")
    elif trigger.nick is owner:
        bot.say("You can't stop a game once started!")



@commands('flee')
def endGame(bot, trigger):
    if ongoing is False:
        if trigger.nick in players:
            players.remove(trigger.nick)
            bot.say(trigger.nick+" has left the game. Coward.")
        else:
            bot.say("You're not signed up you dimwit!")
    else:
        bot.say("The game is still ongoing, you dimwit, you can't leave until Hilter is dead!")


def hitlerGame:
   player_amount = len(players)
   if player_amount < 5:
       return
   elif player_amount > 10:
       return
   else:
       ongoing = True
       while finished is not 1:
