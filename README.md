# secret-hitler-sopel
A module for the Sopel bot to run Secret Hitler in an IRC channel.

The entire game works by changing states that are in a dictionary, the dictionary is going to return to default the new game function is called.


# Rules
http://www.secrethitler.com/assets/Secret_Hitler_Rules.pdf

# Commands

The following commands are available:

.hitler starts a game in the #games channel. If you wish to change the channel, replace any mentions of #games with your channel of choice.

.join and .flee let you join up and quit a game respectively. Only the Owner can .abort. The Owner can be changed in the dictionary at the top of the file.

.start begins a game. It will shuffle the deck. Depending on the amount of players, from 5-6, 7-8 and 9-10 it will have three different board states which affect the special conditions that trigger wen a certain amount of Fascist polices have been enacted.

The randomly chosen president .nominates - the players all vote .yes or .no in PM with the bot. When everyone has voted, the vote is tallied and the next policy will be enacted.

The president receives the top three cards of the deck, then .discards one of them, either Liberal or Fascist. The Chancellor receives two cards and can .enact one of them.

On certain conditions the president can .shoot a player in the channel or .identity them to find out their identity in private.

.policies gives you a count of the policies enacted by now.
