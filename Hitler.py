from sopel.module import commands, require_privmsg
import random


def setup(bot):
    def newGame(bot):
        bot.memory['secret_hitler'] = {'players': [],
                                       'setupPhase': False,
                                       'boardState': None,  # three board states depending on number of players
                                       'liberalPolicies': 0,  # Liberals win with 5 Liberal Policies enacted
                                       'failedElections': 0,  # Maximum of 3 failed Elections, else Chaos
                                       'fascistPolicies': 0,  # Fascists win with 3 Policies and Hitler as Chancellor
                                       'president': None,
                                       'chancellorCandidate': None,
                                       'electionState': False,
                                       'chancellor': None,
                                       'hasVoted': {},
                                       'formerPresident': None,
                                       'formerChancellor': None,
                                       'yesVotes': 0,
                                       'noVotes': 0,
                                       'fascistDeck': 11,
                                       'liberalDeck': 6,
                                       'discardPile': [],
                                       'liberals': [],
                                       'fascists': [],
                                       'dead': [],
                                       'fascistPlayers': 0,
                                       # 2 for 5-6 players, 3 for 7-8 players, 4 for 9-10 players, includes Hitler
                                       'liberalPlayers': 0,
                                       # 3-4 for 5-6 players, 4-5 for 7-8 players, 5-6 for 9-10 players
                                       'Hitler': None,  # randomly chosen among the fascist players
                                       'gameOngoing': False,
                                       'owner': 'VereorNox'}


def assign_fascists(bot, int):
    if len(bot.memory['secret_hitler']['players']) < 5:
        bot.say("Sorry, but not enough players have been gathered.", '#games')
    elif int is 5 or 6:
        bot.memory['secret_hitler']['boardState'] = 0
        bot.memory['secret_hitler']['fascistPlayers'] = 2
    elif int is 7 or 8:
        bot.memory['secret_hitler']['boardState'] = 1
        bot.memory['secret_hitler']['fascistPlayers'] = 3
    elif int is 9 or 10:
        bot.memory['secret_hitler']['boardState'] = 2
        bot.memory['secret_hitler']['fascistPlayers'] = 4
    else:
        bot.say("There are too many players. Please keep it 5 to 10.")
    while len(bot.memory['secret_hitler']['fascists']) < int:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                bot.memory['secret_hitler']['liberals']:
            random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['fascists'])


def assign_liberals(bot, int):
    if int is 5:
        bot.memory['secret_hitler']['liberalPlayers'] = 3
    if int is 6 or 7:
        bot.memory['secret_hitler']['liberalPlayers'] = 4
    if int is 8 or 9:
        bot.memory['secret_hitler']['liberalPlayers'] = 5
    if int is 10:
        bot.memory['secret_hitler']['liberalPlayers'] = 6
    while len(bot.memory['secret_hitler']['liberals']) < 3:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or \
                bot.memory['secret_hitler']['liberals']:
            random.choice(bot.memory['secret_hitler']['players']).append(bot.memory['secret_hitler']['liberals'])


# TODO: MAKE THIS INTO ONE FUNCTION FOR FUCK'S SAKE

def checkVotes(bot, trigger):
    if bot.memory['secret_hitler']['failedVotes'] == 3:
        bot.say("The country is thrown into chaos! Take the top card of the deck and enact that policy!")

@commands('hitler')
def start(bot, trigger):
    if bot.memory['secret_hitler']['gameOngoing'] is False:
        setup.newGame(bot)
        bot.memory['secret_hitler']['setupPhase'] = True
        bot.say(
            "Someone has started a game of Secret Hitler! Type .join to join! When 5 players have assembled, type .start to start!")
        bot.memory['secret_hitler']['players'].append(trigger.nick)
        bot.say(trigger.nick + " has joined up! Type .flee to leave with your tail tucked between your legs!")
    else:
        bot.say("A game is already going on. Please wait until it is finished to start another game.")


@commands('join')
def joinGame(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] is True:
        if trigger.nick not in bot.memory['secret_hitler']['players']:
            bot.memory['secret_hitler']['players'].append(trigger.nick)
            bot.say(trigger.nick + " has joined up!")
        else:
            bot.say(
                "You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!")


@commands('start')
def start(bot, trigger):
    if bot.memory['secret_hitler']['setupPhase'] is True:
        bot.memory['secret_hitler']['setupPhase'] = False
        bot.memory['secret_hitler']['gameOngoing'] = True
        assign_fascists(bot, len(bot.memory['secret_hitler']['players']))
        assign_liberals(bot, len(bot.memory['secret_hitler']['players']))
        for player in bot.memory['secret_hitler']['liberals']:
            bot.say("You're a liberal! Prevent Hitler from taking over by passing five liberal policies!", player)
        for player in bot.memory['secret_hitler']['fascists']:
            bot.say("You're a fascist! Pass three fascist policies and elect Hitler as Chancellor to win!", player)
        bot.memory['secret_hitler']['Hitler'] = random.choice(bot.memory['secret_hitler']['fascists'])
        bot.say(
            "You're also Hitler! Confuse the enemies by pretending to be liberal, trusting your allies to lead you to victory!",
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
            bot.say("You can't nominate yourself, Mr. President.")
        elif trigger.group(2) in bot.memory['secret_hitler']['players']:
            if trigger.group(2) not in bot.memory['secret_hitler']['formerChancellor']:
                bot.memory['secret_hitler']['chancellorCandidate'] = trigger.group(2)
                bot.say(trigger.group(2) + " has been nominated as Chancellor.")
                bot.say("Players, make your choice! Vote .yes or .no in PM with me!")
                bot.memory['secret_hitler']['electionState'] = True
            else:
                bot.say("You cannot elect the same Chancellor twice in succession, there are term limits.")
    else:
        bot.say("You're not the president, " + trigger.nick, '#games')

@require_privmsg
@commands('yes')
def ja(bot, trigger):
    if bot.memory['secret_hitler']['electionState'] is True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['hasVoted']:
                bot.memory['secret_hitler']['yesVotes'] += 1
                bot.memory['secret_hitler']['hasVoted'].update({trigger.nick: 'Yes'})
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)



@require_privmsg
@commands('no')
def nein(bot, trigger):
    if bot.memory['secret_hitler']['electionState'] is True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['hasVoted']:
                bot.memory['secret_hitler']['noVotes'] += 1
                bot.memory['secret_hitler']['hasVoted'].update({trigger.nick: 'No'})
            else:
                bot.say("You're already voted!", trigger.nick)
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)

def tallyVotes(bot, trigger):
    if len(bot.memory['secret_hitler']['hasVoted'].keys()) == len(bot.memory['secret_hitler']['hasVoted'].keys()):
        bot.memory['secret_hitler']['electionState'] = False
        bot.say("The voting has closed!", '#games')
        bot.say(bot.memory['secret_hitler']['hasVoted'], '#games')
        if bot.memory['secret_hitler']['yesVotes'] > bot.memory['secret_hitler']['noVotes']:
            bot.say(bot.memory['secret_hitler']['chancellorCandidate']+" has been elected Chancellor!")
            bot.memory['secret_hitler']['chancellor'] = bot.memory['secret_hitler']['chancellorCandidate']
        else:
            bot.say("The vote has failed! The presidency moves on!")
            bot.memory['secret_hitler']['failedVotes'] += 1
            checkVotes(bot, trigger)






# TODO: LEAVE FUNCTION BEFORE GAME STARTS
# TODO: ABORT FUNCTION TO IMMEDIATELY END GAME
