from sopel.module import commands


@commands('hello')
def hello(bot, trigger):
    bot.say("Hello,", trigger.nick)