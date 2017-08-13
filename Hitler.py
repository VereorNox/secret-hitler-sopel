from sopel.module import commands
import random


def setup(bot):
    def newGame(bot):
        bot.memory['secret_hitler'] = { 'players':[],
                                        'setupPhase':False,
                                        'boardState':None, # three board states depending on number of players
                                        'liberalPolicies':0, # Liberals win with 5 Liberal Policies enacted
                                        'failedElections':0, # Maximum of 3 failed Elections, else Chaos
                                        'fascistPolicies':0, # Fascists win with 3 Policies and Hitler as Chancellor
                                        'president':None,
                                        'chancellorCandidate':None,
                                        'chancellor':None,
                                        'formerPresident':None,
                                        'formerChancellor':None,
                                        'yesVotes':0,
                                        'noVotes':0,
                                        'fascistDeck':11,
                                        'liberalDeck':6,
                                        'liberals':[],
                                        'fascists':[],
                                        'dead':[],
                                        'fascistPlayers':0, # 2 for 5-6 players, 3 for 7-8 players, 4 for 9-10 players, includes Hitler
                                        'liberalPlayers':0, # 3-4 for 5-6 players, 4-5 for 7-8 players, 5-6 for 9-10 players
                                        'Hitler':None, # randomly chosen among the fascist players
                                        'gameOngoing':False,
                                        'owner':'VereorNox' }



def assignPlayers(bot):
    if len(bot.memory['secret_hitler']['players']) < 5:
        bot.say("Sorry, but not enough players have been gathered.", '#games')
    elif len(bot.memory['secret_hitler']['players']) is 5:
        bot.memory['secret_hitler']['boardState'] = 0
        bot.memory['secret_hitler']['liberalPlayers'] = 3
        bot.memory['secret_hitler']['fascistPlayers'] = 2
        while len(bot.memory['secret_hitler']['liberals']) < 3:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 2:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])


    elif len(bot.memory['secret_hitler']['players']) is 6:
        bot.memory['secret_hitler']['boardState'] = 0
        bot.memory['secret_hitler']['liberalPlayers'] = 4
        bot.memory['secret_hitler']['fascistPlayers'] = 2
        while len(bot.memory['secret_hitler']['liberals']) < 4:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 2:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])

    elif len(bot.memory['secret_hitler']['players']) is 7:
        bot.memory['secret_hitler']['boardState'] = 1
        bot.memory['secret_hitler']['liberalPlayers'] = 4
        bot.memory['secret_hitler']['fascistPlayers'] = 3
        while len(bot.memory['secret_hitler']['liberals']) < 4:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 3:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])

    elif len(bot.memory['secret_hitler']['players']) is 8:
        bot.memory['secret_hitler']['boardState'] = 1
        bot.memory['secret_hitler']['liberalPlayers'] = 5
        bot.memory['secret_hitler']['fascistPlayers'] = 3
        while len(bot.memory['secret_hitler']['liberals']) < 5:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 3:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])

    elif len(bot.memory['secret_hitler']['players']) is 9:
        bot.memory['secret_hitler']['boardState'] = 2
        bot.memory['secret_hitler']['liberalPlayers'] = 5
        bot.memory['secret_hitler']['fascistPlayers'] = 4
        while len(bot.memory['secret_hitler']['liberals']) < 5:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 4:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])

    elif len(bot.memory['secret_hitler']['players']) is 10:
        bot.memory['secret_hitler']['boardState'] = 2
        bot.memory['secret_hitler']['liberalPlayers'] = 6
        bot.memory['secret_hitler']['fascistPlayers'] = 4
        while len(bot.memory['secret_hitler']['liberals']) < 6:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])
        while len(bot.memory['secret_hitler']['fascists']) < 4:
            if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                    bot.memory['secret_hitler']['liberals']:
                random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])


@commands('hitler')
def start(bot, trigger):
    if bot.memory['secret_hitler']['gameOngoing'] is False:
        setup.newGame(bot)
        bot.memory['secret_hitler']['setupPhase'] = True
        bot.say("Someone has started a game of Secret Hitler! Type .join to join! When 5 players have assembled, type .start to start!")
        bot.memory['secret_hitler']['players'].append(trigger.nick)
        bot.say(trigger.nick + " has joined up! Type .flee to leave with your tail tucked between your legs!")
    else:
        bot.say("A game is already going on. Please wait until it is finished to start another game.")



@commands('join')
def joinGame(bot, trigger):
    if trigger.nick not in bot.memory['secret_hitler']['players']:
        bot.memory['secret_hitler']['players'].append(trigger.nick)
        bot.say(trigger.nick+" has joined up!")
    else:
        bot.say("You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!")

@commands('start')
def start(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] is True:
        bot.memory['secret_hitler']['setupPhase'] = False
        assignPlayers(bot)
        for player in bot.memory['secret_hitler']['liberals']:
            bot.say("You're a liberal! Prevent Hitler from taking over by passing five liberal policies!", player)
        for player in bot.memory['secret_hitler']['fascists']:
            bot.say("You're a fascist! Pass three fascist policies and elect Hitler as Chancellor to win!", player)
        bot.memory['secret_hitler']['Hitler'] = random.choice(bot.memory['secret_hitler']['fascists'])
        bot.say("You're also Hitler! Confuse the enemies by pretending to be liberal, trusting your allies to lead you to victory!", bot.memory['secret_hitler']['Hitler'])
        bot.say("The assembly of the Reichstag opens!", '#games')
        bot.memory['secret_hitler']['president'] = random.choice(bot.memory['secret_hitler']['players'])
        bot.say(bot.memory['secret_hitler']['president']+" has been elected as President! President, make your choice! Who do you .nominate as Chancellor?")
    else:
        bot.say("No game has been opened yet. Type .hitler to start a game and .start to start once enough players have assembled!")

@commands('nominate')
def nominateChancellor(bot, trigger):
    if trigger.nick is bot.memory['secret_hitler']['president']:
        
    else:
        bot.say("You're not the president, "+trigger.nick, '#games')

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
        if trigger.nick in bot.memory['secret_hitler']['players']:
            bot.memory['secret_hitler']['players'].remove(trigger.nick)
            bot.say(trigger.nick+" has left the game. Coward.")
        else:
            bot.say("You're not signed up you dimwit!")
    else:
        bot.say("The game is still ongoing, you dimwit, you can't leave until Hilter is dead!")




