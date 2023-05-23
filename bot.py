from twitchio.ext import commands

access_token_file = open('../tokens/access.token', 'r')
access_token = access_token_file.read().replace("\n", "") 
access_token_file.close()

from streamGame import ChroniConsole 
import asyncio

from cupGame import CupGame

console_size = (500, 500)

class ChronicoBot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=access_token, prefix='?', initial_channels=['Chronico1'])
        self.console = ChroniConsole(None, console_size)


    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def log(self, ctx: commands.Context):
        await ctx.reply(f'What\'s up loser?')
    
    @commands.command()
    async def cups(self, ctx: commands.Context):
        self.console.eject()
        self.console.insert(CupGame, ctx)
        await self.console.run()
        await self.announce_cups_wins(ctx)
        self.console.eject()

    async def announce_cups_wins(self, ctx):
        winners = self.console.getOutput()
        await ctx.send(f"Congrats to {winners} for winning Cups!")
        return 1 

    @commands.command()
    async def vote(self, ctx: commands.Context, arg=""):
        self.console.pushInput({ctx.author.name: arg})
         


bot = ChronicoBot()

bot.run()
