import discord
from discord.ext import commands
from modules import scrape


class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def about(self, ctx, *, query: str):
        url = scrape.search(query=query)
        about = scrape.scrape_about(url=url)
        await ctx.send(f"```\n{about[0]}```")


def setup(client):
    client.add_cog(Wiki(client))