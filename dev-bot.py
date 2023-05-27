from twitchio.ext import commands

access_token_file = open('../tokens/access.token', 'r')
access_token = access_token_file.read().replace("\n", "") 
access_token_file.close()

from userData import User
from streamGame import ChroniConsole 
import asyncio

from cupGame import CupGame
from duelGame import DuelGame

console_size = (500, 500)

class ChronicoBot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=access_token, prefix='?', initial_channels=['Chronico1'])
        self.console = ChroniConsole(2, None, console_size)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def duel(self, ctx: commands.Context, arg=""):
        if self.console.game != None:
            await ctx.reply("Sorry, the console is currently busy.")
        elif arg == "":
            await ctx.reply("Please specify the player you would like to duel")
        else:
            self.console.eject()
            await ctx.send(f"Halt, @{arg}! {ctx.author.name} has challenged you to a duel! Type ?accept to play.")
            player2 = await self.console.awaitInput("accept", arg)
            if player2 != None:
                self.console.pushInput(ctx.author.name)
                self.console.pushInput(arg)
                await self.console.insert(DuelGame, ctx)
                await self.console.run()
                self.console.eject()
            else:
                await ctx.reply("Sorry. Your opponent did not accept your duel")

    @commands.command()
    async def accept(self, ctx: commands.Context):
        self.console.pushInput({"accept": ctx.author.name})
    
bot = ChronicoBot()

bot.run()
