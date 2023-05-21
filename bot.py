from twitchio.ext import commands

access_token_file = open('../tokens/access.token', 'r')
access_token = access_token_file.read().replace("\n", "") 
access_token_file.close()

from ballCup import CupGame
import asyncio

class ChronicoBot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=access_token, prefix='?', initial_channels=['Chronico1'])
        self.game_playing = False
        self.game_name = ""
        self.votes = {}
        self.winner = None
        self.ctx = None

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
        if not self.game_playing:
            self.game_name = "Cup Game"
            self.game_playing = True
            self.votes = {}
            await ctx.send(f"{ctx.author.name} has started a game of cups!")
            game = CupGame()
            await ctx.send(f"Cast your cups vote when cups stop moving! ?vote (1, 2, or 3)")
            self.winner = None
            
            game.play()
            self.winner = game.end() + 1

            await ctx.send(f"The winning cup was number {self.winner}!")
            self.ctx = ctx
            await self.announce_winners()
            self.game_playing = False
    
    @commands.command()
    async def vote(self, ctx: commands.Context, arg=""):
        self.ctx = ctx
        self.votes[ctx.author.name] = arg
        print('arg:', arg)
        print('winning:', self.winner)
        if arg == "" or arg == "None":
            await ctx.reply(f"Your vote is missing a value!")
        elif arg == str(self.winner):
            await ctx.reply(f"Congrats! You won {self.game_name}!")

    async def announce_winners(self):
        if self.game_playing:
            for voter in self.votes:
                if self.votes[voter] == str(self.winner):
                    await self.ctx.send(f"Congrats! @{voter} has won {self.game_name}!")
                

bot = ChronicoBot()

bot.run()
