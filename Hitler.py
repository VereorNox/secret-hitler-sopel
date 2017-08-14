from sopel.module import commands, require_privmsg
import random


def newgame(bot):
    bot.memory['secret_hitler'] = {'players': ['A', 'B', 'C', 'D', 'E'],
                                   'setup_phase': False,
                                   'board_state': 0,  # three board states depending on number of players
                                   'liberal_policies': 0,  # Liberals win with 5 Liberal Policies enacted
                                   'failed_votes': 0,  # Maximum of 3 failed Elections, else Chaos
                                   'fascist_policies': 0,  # Fascists win with 3 Policies and Hitler as Chancellor
                                   'president': None,
                                   'chancellor_candidate': None,
                                   'former_president': None, # necessary for the special election process
                                   'election_phase': False,
                                   'chancellor': None,
                                   'players_who_voted': {},
                                   'former_chancellor': None,
                                   'yes_votes': 0,
                                   'no_votes': 0,
                                   'deck':['Liberal', 'Liberal', 'Liberal', 'Liberal', 'Liberal', 'Liberal', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist', 'Fascist'],
                                   'drawn_cards':[],
                                   'discard_pile': [],
                                   'liberals': [],
                                   'fascists': [],
                                   'kill_phase': False,
                                   'vote_phase': False,
                                   'reveal_phase': False,
                                   'special_election_phase': False,
                                   'chaos_phase': False,
                                   'veto_switch': False,
                                   'policy_phase': False,
                                   'dead_players': [],
                                   'num_of_fascists': 0,
                                   # 2 for 5-6 players, 3 for 7-8 players, 4 for 9-10 players, includes Hitler
                                   'num_of_liberals': 0,
                                   # 3-4 for 5-6 players, 4-5 for 7-8 players, 5-6 for 9-10 players
                                   'Hitler': None,  # randomly chosen among the fascist players
                                   'game_ongoing': False,
                                   'owner': 'VereorNox'}


def assign_fascists(bot, n):
    """Assigns random fascists until the number of fascists is full."""
    if n is 5 or 6:
        bot.memory['secret_hitler']['board_state'] = 0
        bot.memory['secret_hitler']['num_of_fascists'] = 2
    elif n is 7 or 8:
        bot.memory['secret_hitler']['board_state'] = 1
        bot.memory['secret_hitler']['num_of_fascists'] = 3
    elif n is 9 or 10:
        bot.memory['secret_hitler']['board_state'] = 2
        bot.memory['secret_hitler']['num_of_fascists'] = 4
    while bot.memory['secret_hitler']['num_of_fascists'] <= n:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or bot.memory['secret_hitler']['liberals']:
            bot.memory['secret_hitler']['fascists'].append(random.choice(bot.memory['secret_hitler']['players']))



def assign_liberals(bot, n):
    if n is 5:
        bot.memory['secret_hitler']['num_of_liberals'] = 3
    if n is 6 or 7:
        bot.memory['secret_hitler']['num_of_liberals'] = 4
    if n is 8 or 9:
        bot.memory['secret_hitler']['num_of_liberals'] = 5
    if n is 10:
        bot.memory['secret_hitler']['num_of_liberals'] = 6
    while bot.memory['secret_hitler']['num_of_liberals'] <= n:
        if bot.memory['secret_hitler']['players'] not in bot.memory['secret_hitler']['fascists'] or bot.memory['secret_hitler']['liberals']:
            bot.memory['secret_hitler']['liberals'].append(random.choice(bot.memory['secret_hitler']['players']))


def checkVotes(bot, trigger):
    if bot.memory['secret_hitler']['failed_votes'] == 3:
        bot.say("The country is thrown into chaos! Take the top card of the deck and enact that policy!", '#games')
        bot.memory['secret_hitler']['chaos_state'] = True

@require_privmsg
@commands('discard')
def pickCard(bot, trigger):
    if trigger.nick is not bot.memory['secret_hitler']['president']:
        bot.say("You can't pick anything if you can't see anything.")
    elif trigger.group(2) not in bot.memory['secret_hitler']['drawn_cards']:
        bot.say("Mr. President, you have to discard a card that was picked.", trigger.nick)
    else:
        bot.memory['secret_hitler']['discard_pile'].append(bot.memory['secret_hitler']['drawn_cards'][trigger.group(2)])
        bot.memory['secret_hitler']['drawn_cards'].remove(trigger.group(2))
        bot.say("The president has discarded a card. Enact the one you want with .enact [card]!",
                bot.memory['secret_hitler']['chancellor'])

def board_state(bot, trigger):
    if bot.memory['secret_hitler']['board_state'] == 0:
        if bot.memory['secret_hitler']['fascist_policies'] == 3:
            bot.say("Pssst, these are the top three cards: "+bot.memory['secret_hitler']['deck'][0]+bot.memory['secret_hitler']['deck'][1]+bot.memory['secret_hitler']['deck'][2])
        elif bot.memory['secret_hitler']['fascist_policies'] == 4:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
        elif bot.memory['secret_hitler']['fascist_policies'] == 5:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.memory['secret_hitler']['veto_switch'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
            bot.say("You have unlocked veto power! After giving the Chancellor two cards, they may declare a .veto!", '#games')
        else:
            turn(bot, trigger)
    elif bot.memory['secret_hitler']['board_state'] == 1:
        if bot.memory['secret_hitler']['fascist_policies'] == 2:
            bot.memory['secret_hitler']['reveal_phase'] = True
        elif bot.memory['secret_hitler']['fascist_policies'] == 3:
            bot.memory['secret_hitler']['special_election_phase'] = True
        elif bot.memory['secret_hitler']['fascist_policies'] == 4:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
        elif bot.memory['secret_hitler']['fascist_policies'] == 5:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.memory['secret_hitler']['veto_switch'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
            bot.say("You have unlocked veto power! After giving the Chancellor two cards, they may declare a .veto!", '#games')
        else:
            turn(bot, trigger)
    elif bot.memory['secret_hitler']['board_state'] == 2:
        if bot.memory['secret_hitler']['fascist_policies'] == 1:
            bot.memory['secret_hitler']['reveal_phase'] = True
        elif bot.memory['secret_hitler']['fascist_policies'] == 2:
            bot.memory['secret_hitler']['reveal_phase'] = True
        elif bot.memory['secret_hitler']['fascist_policies'] == 3:
            bot.memory['secret_hitler']['special_election_phase'] = True
        elif bot.memory['secret_hitler']['fascist_policies'] == 4:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
        elif bot.memory['secret_hitler']['fascist_policies'] == 5:
            bot.memory['secret_hitler']['kill_phase'] = True
            bot.memory['secret_hitler']['veto_switch'] = True
            bot.say("The fascists are getting dangerous! Mr. President, .shoot someone to order their execution!", '#games')
            bot.say("You have unlocked veto power! After giving the Chancellor two cards, they may declare a .veto!", '#games')
        else:
            turn(bot, trigger)

@commands('endorse')
def special_election(bot, trigger):
    if bot.memory['secret_hitler']['special_election_phase'] == True and trigger.nick == bot.memory['secret_hitler']['president']:
        if trigger.group(2) != bot.memory['secret_hitler']['president']:
            bot.memory['secret_hitler']['former_president'] = bot.memory['secret_hitler']['president']
            bot.memory['secret_hitler']['president'] = trigger.group(2)
            bot.say(trigger.group(2)+" has been made president after a special election! Make your choice, president, who do you propose as chancellor?")
            bot.memory['secret_hitler']['election_phase'] = True
        else:
            bot.say("You can't choose yourself to be president again, there are term limits!", '#games')


@commands('veto')
def veto(bot, trigger):
    if bot.memory['secret_hitler']['vetoPhase'] == True:
        if bot.memory['secret_hitler']['policy_phase'] == True and trigger.nick == bot.memory['secret_hitler']['chancellor']:
            bot.say("The chancellor has called for a veto! Herr President only has to agree to discard both cards! .veto or .noveto?", '#games')
            global vetoState
            vetoState = True
        if trigger.nick == bot.memory['secret_hitler']['president'] and vetoState == True:
            bot.say("The policies are all discarded!", '#games')
            bot.memory['secret_hitler']['discard_pile'].append(bot.memory['secret_hitler']['drawn_cards'])
            del bot.memory['secret_hitler']['drawn_cards'][:]
            turn(bot, trigger)
    else:
        bot.say("Nobody can veto as of yet.", '#games')

@commands('noveto')
def no_veto(bot, trigger):
    if trigger.nick == bot.memory['secret_hitler']['president'] and vetoState == True:
        bot.say("I'm afraid you have to enact a policy, Mr. Chancellor!", '#games')


def turn(bot, trigger):
    if bot.memory['secret_hitler']['next_turn'] == True:
        bot.say("The next turn has started!", '#games')
        index = bot.memory['secret_hitler']['players'].index(bot.memory['secret_hitler']['president'])
        if bot.memory['secret_hitler']['special_election_phase'] == True:
            bot.memory['secret_hitler']['president'] = bot.memory['secret_hitler']['former_president']
            bot.memory['secret_hitler']['president'] = bot.memory['secret_hitler']['players'][index % len(bot.memory['secret_hitler']['players'])]
        else:
            bot.memory['secret_hitler']['president'] = bot.memory['secret_hitler']['players'][index % len(bot.memory['secret_hitler']['players'])]
        bot.memory['secret_hitler']['former_chancellor'] = bot.memory['secret_hitler']['chancellor']
        bot.memory['secret_hitler']['election_phase'] = True
        bot.memory['secret_hitler']['vote_phase'] = False
        bot.memory['secret_hitler']['kill_phase'] = False
        bot.memory['secret_hitler']['special_election_phase'] = False
        bot.memory['secret_hitler']['reveal_phase'] = False
        bot.memory['secret_hitler']['policy_phase'] = False
        bot.say(bot.memory['secret_hitler']['president']+" has been elected President! Mr. President, make your choice! Who do you nominate as Chancellor?", '#games')


@require_privmsg
@commands('enact')
def enactPolicy(bot, trigger):
    if trigger.nick is not bot.memory['secret_hitler']['chancellor']:
        bot.say("You're not the Chancellor. Piss off.")
    elif trigger.group(2) not in bot.memory['secret_hitler']['drawn_cards']:
        bot.say("Herr Chancellor, you have to discard a card that was picked.", trigger.nick)
    else:
        if trigger.group(2) == 'Liberal':
            bot.say("The enacted policy is Liberal!", '#games')
            bot.memory['secret_hitler']['liberal_policies'] += 1
            del bot.memory['secret_hitler']['drawn_cards'][trigger.group(2)]
            bot.memory['secret_hitler']['discard_pile'].append(bot.memory['secret_hitler']['drawn_cards'])
            del bot.memory['secret_hitler']['drawn_cards'][:]
            turn(bot, trigger)
        else:
            bot.say("The enacted policy is Fascist!", '#games')
            bot.memory['secret_hitler']['fascist_policies'] += 1
            del bot.memory['secret_hitler']['drawn_cards'][trigger.group(2)]
            bot.memory['secret_hitler']['discard_pile'].append(bot.memory['secret_hitler']['drawn_cards'])
            del bot.memory['secret_hitler']['drawn_cards'][:]
            board_state(bot, trigger)


@commands('hitler')
def prepare_to_start(bot, trigger):
    print(bot.memory.keys())
    print("HITLER!")
    if 'secret_hitler' not in bot.memory or bot.memory['secret_hitler']['game_ongoing'] is False:
        newgame(bot)
        random.shuffle(bot.memory['secret_hitler']['deck'])
        bot.memory['secret_hitler']['setup_phase'] = True
        bot.say("Someone has started a game of Secret Hitler! Type .join to join! When 5 players have assembled, type .start to start!", '#games')
        bot.memory['secret_hitler']['players'].append(trigger.nick)
        bot.say(trigger.nick + " has joined up! Type .flee to leave with your tail tucked between your legs!", '#games')
    else:
        bot.say("A game is already going on. Please wait until it is finished to start another game.", '#games')
    print("HITLEEEEER!")


@commands('join')
def joinGame(bot, trigger):
    if bot.memory['secret_hitler']['setup_phase'] == True:
        if trigger.nick not in bot.memory['secret_hitler']['players'] and len(bot.memory['secret_hitler']['players']) < 10:
            bot.memory['secret_hitler']['players'].append(trigger.nick)
            bot.say(trigger.nick + " has joined up!", '#games')
            bot.say("You need at least 5 players to start the game!", '#games')
            bot.say(str(len(bot.memory['secret_hitler']['players']))+" have already signed up!", '#games')
        else:
            bot.say(
                "You're already signed up for the game! Type .flee to leave with your tail tucked between your legs!", '#games')


@commands('start')
def startingGame(bot, trigger):
    if bot.memory['secret_hitler']['setup_phase'] == True:
        if len(bot.memory['secret_hitler']['players']) < 5 or len(bot.memory['secret_hitler']['players']) > 10:
            bot.say("Not enough or too many players. 5-10 is acceptable.", '#games')
            return
        bot.memory['secret_hitler']['setup_phase'] = False
        bot.memory['secret_hitler']['game_ongoing'] = True
        print("VERN!")
        assign_fascists(bot, len(bot.memory['secret_hitler']['players']))
        print("TUZI!")
        assign_liberals(bot, len(bot.memory['secret_hitler']['players']))
        print("NICK!")
        for player in bot.memory['secret_hitler']['liberals']:
            bot.say("You're a liberal! Prevent Hitler from taking over by passing five liberal policies!", player)
            print("A B C")
        for player in bot.memory['secret_hitler']['fascists']:
            bot.say("You're a fascist! Pass three fascist policies and elect Hitler as Chancellor to win!", player)
            print("D E F")
        bot.memory['secret_hitler']['Hitler'] = random.choice(bot.memory['secret_hitler']['fascists'])
        for player in bot.memory['secret_hitler']['fascists']:
            if len(bot.memory['secret_hitler']['players']) >= 7:
                if player != bot.memory['secret_hitler']['Hitler']:
                    bot.say("The other fascists are"+bot.memory['secret_hitler']['fascists'], player)
                    bot.say(bot.memory['secret_hitler']['Hitler']+"is Hitler!", player)
            else:
                bot.say("The other fascists are" + bot.memory['secret_hitler']['fascists'], player)
                bot.say(bot.memory['secret_hitler']['Hitler'] + "is Hitler!", player)
        bot.say(
            "You're Hitler! Confuse the enemies by pretending to be liberal, trusting your allies to lead you to victory!",
            bot.memory['secret_hitler']['Hitler'])
        bot.say("The assembly of the Reichstag opens!", '#games')
        bot.memory['secret_hitler']['president'] = random.choice(bot.memory['secret_hitler']['players'])
        bot.say(bot.memory['secret_hitler'][
                    'president'] + " has been elected as President! President, make your choice! Who do you .nominate as Chancellor?", '#games')
        bot.memory['secret_hitler']['election_phase'] = True
    else:
        bot.say(
            "No game has been opened yet. Type .hitler to start a game and .start to start once enough players have assembled!", '#games')


@commands('nominate')
def nominateChancellor(bot, trigger):
    if trigger.nick is bot.memory['secret_hitler']['president']:
        if trigger.group(2) in bot.memory['secret_hitler']['president']:
            bot.say("You can't nominate yourself, Mr. President.", '#games')
        elif trigger.group(2) in bot.memory['secret_hitler']['players']:
            if trigger.group(2) not in bot.memory['secret_hitler']['former_chancellor']:
                bot.memory['secret_hitler']['election_phase'] = False
                bot.memory['secret_hitler']['chancellor_candidate'] = trigger.group(2)
                bot.say(trigger.group(2) + " has been nominated as Chancellor.", '#games')
                bot.say("Players, make your choice! Vote .yes or .no in PM with me!", '#games')
                bot.memory['secret_hitler']['vote_phase'] = True
            else:
                bot.say("You cannot elect the same Chancellor twice in succession, there are term limits.", '#games')
    else:
        bot.say("You're not the president, " + trigger.nick, '#games')

@require_privmsg
@commands('yes')
def ja(bot, trigger):
    if bot.memory['secret_hitler']['vote_phase'] == True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['players_who_voted']:
                bot.memory['secret_hitler']['yes_votes'] += 1
                bot.memory['secret_hitler']['players_who_voted'].update({trigger.nick: 'Yes'})
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)



@require_privmsg
@commands('no')
def nein(bot, trigger):
    if bot.memory['secret_hitler']['vote_phase'] == True:
        if trigger.nick in bot.memory['secret_hitler']['players']:
            if trigger.nick not in bot.memory['secret_hitler']['players_who_voted']:
                bot.memory['secret_hitler']['no_votes'] += 1
                bot.memory['secret_hitler']['players_who_voted'].update({trigger.nick: 'No'})
            else:
                bot.say("You're already voted!", trigger.nick)
        else:
            bot.say("You're not a player you fuckwit!", trigger.nick)

def tallyVotes(bot, trigger):
    if len(bot.memory['secret_hitler']['players_who_voted']) == len(bot.memory['secret_hitler']['players']):
        bot.memory['secret_hitler']['vote_phase'] = False
        bot.say("The voting has closed!", '#games')
        bot.say(bot.memory['secret_hitler']['players_who_voted'], '#games')
        del bot.memory['secret_hitler']['players_who_voted']
        if bot.memory['secret_hitler']['yes_votes'] > bot.memory['secret_hitler']['no_votes']:
            bot.say(bot.memory['secret_hitler']['chancellor_candidate']+" has been elected Chancellor!", '#games')
            bot.memory['secret_hitler']['chancellor'] = bot.memory['secret_hitler']['chancellor_candidate']
            if bot.memory['secret_hitler']['chancellor'] == bot.memory['secret_hitler']['Hitler'] and bot.memory['secret_hitler']['fascist_policies'] >= 3:
                bot.say("A man takes the podium, his face slowly falling off to reveal an ancient evil with toothbrush "
                        "beard. Hitler has taken over, and the government is overthrown by his party.", '#games')
                bot.memory['secret_hitler']['game_ongoing'] = False
                return

            bot.say("The next policy is going to be enacted!")
            bot.memory['secret_hitler']['drawn_cards'].append(bot.memory['secret_hitler']['deck'][0])
            bot.memory['secret_hitler']['drawn_cards'].append(bot.memory['secret_hitler']['deck'][1])
            bot.memory['secret_hitler']['drawn_cards'].append(bot.memory['secret_hitler']['deck'][2])
            del bot.memory['secret_hitler']['deck'][0]
            del bot.memory['secret_hitler']['deck'][1]
            del bot.memory['secret_hitler']['deck'][2]
            bot.say("Pick one of these cards with .discard [card]:"+bot.memory['secret_hitler']['drawn_cards'])

        else:
            bot.say("The vote has failed! The presidency moves on!", '#games')
            bot.memory['secret_hitler']['failed_votes'] += 1
            checkVotes(bot, trigger)
            if  bot.memory['secret_hitler']['chaos_phase'] == True:
                    bot.memory['secret_hitler']['failed_votes'] = 0
                    nextPolicy = bot.memory['secret_hitler']['deck'][0]
                    bot.memory['secret_hitler']['discard_pile'].append(bot.memory['secret_hitler']['deck'][0])
                    del bot.memory['secret_hitler']['deck'][0]
                    if nextPolicy is 'Liberal':
                        bot.say("The enacted policy is Liberal!", '#games')
                        bot.memory['secret_hitler']['liberal_policies'] += 1
                        if bot.memory['secret_hitler']['liberal_policies'] == 5:
                            bot.say("You've done it! The fascists are incapable of taking over the government due to "
                                    "your new policies!")
                            bot.memory['secret_hitler']['game_ongoing'] = False
                            return
                        else:
                            turn(bot, trigger)
                    else:
                        bot.say("The enacted policy is Fascist!", '#games')
                        bot.memory['secret_hitler']['fascist_policies'] += 1
                        board_state(bot, trigger)
                    bot.memory['secret_hitler']['chaos_phase'] = False

@commands('identity')
def reveal_identity(bot, trigger):
    if trigger.nick in bot.memory['secret_hitler']['president'] and bot.memory['secret_hitler']['reveal_phase'] == True:
        if trigger.group(2) in bot.memory['secret_hitler']['liberals']:
            bot.say("The identity of "+trigger.group(2)+" is... Liberal!", trigger.nick)
            bot.memory['secret_hitler']['reveal_phase'] = False
            turn(bot, trigger)
        elif trigger.group(2) in bot.memory['secret_hitler']['fascists']:
            bot.say("The identity of "+trigger.group(2)+" is... Fascist!", trigger.nick)
            bot.memory['secret_hitler']['reveal_phase'] = False
            turn(bot, trigger)
        else:
            bot.say("That's not a player available to reveal!")


@commands('flee')
def flee(bot, trigger):
    if bot.memory['secret_hitler']['setup_phase'] == True and trigger.nick in bot.memory['secret_hitler']['players']:
        bot.memory['secret_hitler']['players'].remove(trigger.nick)
        bot.say(trigger.nick+" has deserted. The new government will court martial them at a later date.")
    else:
        bot.say("The game is going on or you're not signed up! Please wait until the game is over to desert!")


@commands('shoot')
def kill(bot, trigger):
    if trigger.nick is bot.memory['secret_hitler']['president'] and bot.memory['secret_hitler']['kill_phase'] == True:
        bot.memory['secret_hitler']['dead_players'].append(trigger.group(2))
        if trigger.group(2) in bot.memory['secret_hitler']['fascists']:
            bot.say(trigger.group(2)+" has been executed by the order of the president...")
            bot.memory['secret_hitler']['fascists'].remove(trigger.group(2))
            turn(bot, trigger)
        elif trigger.group(2) in bot.memory['secret_hitler']['liberals']:
            bot.say(trigger.group(2)+" has been executed by the order of the president...")
            bot.memory['secret_hitler']['liberals'].remove(trigger.group(2))
            turn(bot, trigger)

@commands('abort')
def abortGame(bot, trigger):
    if trigger.nick == bot.memory['secret_hitler']['owner']:
        bot.say("The game has been stopped by the administration. To start a new game, type .hitler", '#games')
        bot.memory['secret_hitler']['game_ongoing'] = False
        newgame(bot)
        bot.memory['secret_hitler']['setup_phase'] = False
