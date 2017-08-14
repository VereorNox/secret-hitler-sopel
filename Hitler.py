from sopel.module import commands, require_privmsg
import random


def newgame(bot):
    bot.memory['secret_hitler'] = {'players': [],
                                   'setupPhase': False,
                                   'boardState': None,  # three board states depending on number of players
                                   'liberalPolicies': 0,  # Liberals win with 5 Liberal Policies enacted
                                   'failedVotes': 0,  # Maximum of 3 failed Elections, else Chaos
                                   'fascistPolicies': 0,  # Fascists win with 3 Policies and Hitler as Chancellor
                                   'president': None,
                                   'chancellorCandidate': None,
                                   'electionState': False,
                                   'chancellor': None,
                                   'players_who_voted': {},
                                   'formerPresident': None,
                                   'formerChancellor': None,
                                   'yesVotes': 0,
                                   'noVotes': 0,
                                   'deck':['Liberal', 'Liberal', 'Liberal', 'Liberal', 'Liberal', 'Liberal', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist'],
                                   'drawnCards':[],
                                   'discardPile': [],
                                   'liberals': [],
                                   'fascists': [],
                                   'killSwitch': False,
                                   'deadPlayers': [],
                                   'numOfFascists': 0,
                                   # 2 for 5-6 players, 3 for 7-8 players, 4 for 9-10 players, includes Hitler
                                   'numOfLiberals': 0,
                                   # 3-4 for 5-6 players, 4-5 for 7-8 players, 5-6 for 9-10 players
                                   'Hitler': None,  # randomly chosen among the fascist players
                                   'gameOngoing': False,
                                   'owner': 'VereorNox'}


def assign_fascists(bot, int):
    if int is 5 or 6:
        bot.memory['secret_hitler']['boardState'] = 0
        bot.memory['secret_hitler']['numOfFascists'] = 2
    elif int is 7 or 8:
        bot.memory['secret_hitler']['boardState'] = 1
        bot.memory['secret_hitler']['numOfFascists'] = 3
    elif int is 9 or 10:
        bot.memory['secret_hitler']['boardState'] = 2
        bot.memory['secret_hitler']['numOfFascists'] = 4
    while len(bot.memory['secret_hitler']['fascists']) < int:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                bot.memory['secret_hitler']['liberals']:
            bot.memory['secret_hitler']['fascists'].append(random.choice(bot.memory['secret_hitler']['players']))


def assign_liberals(bot, int):
    if int is 5:
        bot.memory['secret_hitler']['numOfLiberals'] = 3
    if int is 6 or 7:
        bot.memory['secret_hitler']['numOfLiberals'] = 4
    if int is 8 or 9:
        bot.memory['secret_hitler']['numOfLiberals'] = 5
    if int is 10:
        bot.memory['secret_hitler']['numOfLiberals'] = 6
    while len(bot.memory['secret_hitler']['liberals']) < int:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                bot.memory['secret_hitler']['liberals']:
            bot.memory['secret_hitler']['liberals'].append(random.choice(bot.memory['secret_hitler']['players']))


# TODO: MAKE THIS INTO ONE FUNCTION FOR FUCK'S SAKE

def checkVotes(bot, trigger):
    if bot.memory['secret_hitler']['failedVotes'] == 3:
        bot.say("The country is thrown into chaos! Take the top card of the deck and enact that policy!", '#games')
        return True
    else:
        return False

@require_privmsg
@commands('discard')
def pickCard(bot, trigger):
    if trigger.nick is not bot.memory['secret_hitler']['president']:
        bot.say("You can't pick anything if you can't see anything.")
    elif trigger.group(2) not in bot.memory['secret_hitler']['drawnCards']:
        bot.say("Mr. President, you have to discard a card that was picked.", trigger.nick)
    else:
        bot.memory['secret_hitler']['discardPile'].append(bot.memory['secret_hitler']['drawnCards'][trigger.group(2)])
        bot.memory['secret_hitler']['drawnCards'].remove(trigger.group(2))
        bot.say("The president has discarded a card. Enact the one you want with .enact [card]!",
                bot.memory['secret_hitler']['chancellor'])

@require_privmsg
@commands('enact')
def enactPolicy(bot, trigger):
    if trigger.nick is not bot.memory['secret_hitler']['chancellor']:
        bot.say("You're not the Chancellor. Piss off.")
    elif trigger.group(2) not in bot.memory['secret_hitler']['drawnCards']:
        bot.say("Herr Chancellor, you have to discard a card that was picked.", trigger.nick)
    else:
        if trigger.group(2) == 'Liberal':
            bot.memory['secret_hitler']['liberalPolicies'] += 1
            del bot.memory['secret_hitler']['drawnCards'][trigger.group(2)]
            bot.memory['secret_hitler']['discardPile'].append(bot.memory['secret_hitler']['drawnCards'])
            del bot.memory['secret_hitler']['drawnCards'][:]
        else:
            bot.memory['secret_hitler']['fascistPolicies'] += 1
            del bot.memory['secret_hitler']['drawnCards'][trigger.group(2)]
            bot.memory['secret_hitler']['discardPile'].append(bot.memory['secret_hitler']['drawnCards'])
            del bot.memory['secret_hitler']['drawnCards'][:]


@commands('hitler')
def prepare_to_start(bot, trigger):
    print(bot.memory.keys())
    print("HITLER!")
    if 'secret_hitler' not in bot.memory or bot.memory['secret_hitler']['gameOngoing'] is False:
        newgame(bot)
        random.shuffle(bot.memory['secret_hitler']['deck'])
        bot.memory['secret_hitler']['setupPhase'] = True
        bot.say("Someone has started a game of Secret Hitler! Type .join to join! When 5 players have assembled, type .start to start!", '#games')
        bot.memory['secret_hitler']['players'].append(trigger.nick)
        bot.say(trigger.nick + " has joined up! Type .flee to leave with your tail tucked between your legs!", '#games')
    else:
        bot.say("A game is already going on. Please wait until it is finished to start another game.", '#games')
    print("HITLEEEEER!")


@commands('join')
def joinGame(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] == True:
        if trigger.nick not in bot.memory['secret_hitler']['players'] and len(bot.memory['secret_hitler']['players']) < 10:
            bot.memory['secret_hitler']['players'].append(trigger.nick)
            bot.say(trigger.nick + " has joined up!")
            bot.say("You need at least "+(5-len(bot.memory['secret_hitler']['players']))+" more players to start the game!")
        else:
            bot.say(
                "You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!", '#games')


@commands('start')
def startingGame(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] == True:
        if len(bot.memory['secret_hitler']['players']) < 5 or len(bot.memory['secret_hitler']['players']) > 10:
            bot.say("Not enough or too many players. 5-10 is acceptable.", '#games')
            return
        bot.memory['secret_hitler']['setupPhase'] = False
        bot.memory['secret_hitler']['gameOngoing'] = True
        assign_fascists(bot, len(bot.memory['secret_hitler']['players']))
        assign_liberals(bot, len(bot.memory['secret_hitler']['players']))
        for player in bot.memory['secret_hitler']['liberals']:
            bot.say("You're a liberal! Prevent Hitler from taking over by passing five liberal policies!", player)
        for player in bot.memory['secret_hitler']['fascists']:
            bot.say("You're a fascist! Pass three fascist policies and elect Hitler as Chancellor to win!", player)
        bot.memory['secret_hitler']['Hitler'] = random.choice(bot.memory['secret_hitler']['fascists'])
        for player in bot.memory['secret_hitler']['fascists']:
            if len(bot.memory['secret_hitler']['players']) >= 7:
                if player != bot.memory['secret_hitler']['Hitler']:
                    bot.say("The other fascists are"+bot.memory['secret_hitler']['fascists'])
                    bot.say(bot.memory['secret_hitler']['Hitler']+"is Hitler!", player)
            else:
                bot.say("The other fascists are" + bot.memory['secret_hitler']['fascists'])
                bot.say(bot.memory['secret_hitler']['Hitler'] + "is Hitler!")
        bot.say(
            "You're Hitler! Confuse the enemies by pretending to be liberal, trusting your allies to lead you to victory!",
            bot.memory['secret_hitler']['Hitler'])
        bot.say("The assembly of the Reichstag opens!", '#games')
        bot.memory['secret_hitler']['president'] = random.choice(bot.memory['secret_hitler']['players'])
        bot.say(bot.memory['secret_hitler'][
                    'president'] + " has been elected as President! President, make your choice! Who do you .nominate as Chancellor?")
    else:
        bot.say(
            "No game has been opened yet. Type .hitler to start a game and .start to start once enough players have assembled!")


@commands('nominate')
def nominateChancellor(bot, trigger):
    if trigger.nick is bot.memory['secret_hitler']['president']:
        if trigger.group(2) in bot.memory['secret_hitler']['president']:
            bot.say("You can't nominate yourself, Mr. President.", '#games')
        elif trigger.group(2) in bot.memory['secret_hitler']['players']:
            if trigger.group(2) not in bot.memory['secret_hitler']['formerChancellor']:
                bot.memory['secret_hitler']['chancellorCandidate'] = trigger.group(2)
                bot.say(trigger.group(2) + " has been nominated as Chancellor.")
                bot.say("Players, make your choice! Vote .yes or .no in PM with me!", '#games')
                bot.memory['secret_hitler']['electionState'] = True
            else:
                bot.say("You cannot elect the same Chancellor twice in succession, there are term limits.", '#games')
    else:
        bot.say("You're not the president, " + trigger.nick, '#games')

@require_privmsg
@commands('yes')
def ja(bot, trigger):
    if bot.memory['secret_hitler']['electionState'] == True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['players_who_voted']:
                bot.memory['secret_hitler']['yesVotes'] += 1
                bot.memory['secret_hitler']['players_who_voted'].update({trigger.nick: 'Yes'})
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)



@require_privmsg
@commands('no')
def nein(bot, trigger):
    if bot.memory['secret_hitler']['electionState'] == True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['players_who_voted']:
                bot.memory['secret_hitler']['noVotes'] += 1
                bot.memory['secret_hitler']['players_who_voted'].update({trigger.nick: 'No'})
            else:
                bot.say("You're already voted!", trigger.nick)
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)

def tallyVotes(bot, trigger):
    if len(bot.memory['secret_hitler']['players_who_voted'].keys()) == len(bot.memory['secret_hitler']['players_who_voted'].keys()):
        bot.memory['secret_hitler']['electionState'] = False
        bot.say("The voting has closed!", '#games')
        bot.say(bot.memory['secret_hitler']['players_who_voted'], '#games')
        if bot.memory['secret_hitler']['yesVotes'] > bot.memory['secret_hitler']['noVotes']:
            bot.say(bot.memory['secret_hitler']['chancellorCandidate']+" has been elected Chancellor!", '#games')
            bot.memory['secret_hitler']['chancellor'] = bot.memory['secret_hitler']['chancellorCandidate']
            bot.say("The next policy is going to be enacted!")
            bot.memory['secret_hitler']['drawnCards'].append(bot.memory['secret_hitler']['deck'][0])
            bot.memory['secret_hitler']['drawnCards'].append(bot.memory['secret_hitler']['deck'][1])
            bot.memory['secret_hitler']['drawnCards'].append(bot.memory['secret_hitler']['deck'][2])
            del bot.memory['secret_hitler']['deck'][0]
            del bot.memory['secret_hitler']['deck'][1]
            del bot.memory['secret_hitler']['deck'][2]
            bot.say("Pick one of these cards with .discard [card]:"+bot.memory['secret_hitler']['drawnCards'])

        else:
            bot.say("The vote has failed! The presidency moves on!", '#games')
            bot.memory['secret_hitler']['failedVotes'] += 1
            if checkVotes(bot, trigger):
                bot.memory['secret_hitler']['failedVotes'] = 0
                nextPolicy = bot.memory['secret_hitler']['deck'][0]
                bot.memory['secret_hitler']['discardPile'].append(bot.memory['secret_hitler']['deck'][0])
                del bot.memory['secret_hitler']['deck'][0]
                if nextPolicy is 'Liberal':
                    bot.memory['secret_hitler']['liberalPolicies'] += 1
                else:
                    bot.memory['secret_hitler']['fascistPolicies'] += 1


@commands('flee')
def flee(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] == True and trigger.nick in bot.memory['secret_hitler']['players']:
        bot.memory['secret_hitler']['players'].remove(trigger.nick)
        bot.say(trigger.nick+" has deserted. The new government will court martial them at a later date.")
    else:
        bot.say("The game is going on or you're not signed up! Please wait until the game is over to desert!")


@commands('shoot')
def kill(bot, trigger):
    if trigger.nick is bot.memory['secret_hitler']['president'] and bot.memory['secret_hitler']['killSwitch'] == True:
        bot.memory['secret_hitler']['deadPlayers'].append(trigger.group(2))
        if trigger.group(2) in bot.memory['secret_hitler']['fascists']:
            bot.say(trigger.group(2)+" has been executed by the order of the president...")
            bot.memory['secret_hitler']['fascists'].remove(trigger.group(2))
        elif trigger.group(2) in bot.memory['secret_hitler']['liberals']:
            bot.say(trigger.group(2)+" has been executed by the order of the president...")
            bot.memory['secret_hitler']['liberals'].remove(trigger.group(2))



# TODO: LEAVE FUNCTION BEFORE GAME STARTS
# TODO: ABORT FUNCTION TO IMMEDIATELY END GAME
