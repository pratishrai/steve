import discord
from discord.ext import commands
from modules import scrape


class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def about(self, ctx, *, query: str):
        async with ctx.channel.typing():
            url = scrape.search(query=query)
            title, about, image = scrape.scrape_about(url=url)
            image = image.split("/revision")
            title = title.split("–")
            embed = discord.Embed(
                title=f"{title[0]}",
                colour=ctx.author.colour,
                description=f"{about[0]}\n{about[1]}\n{about[2]}",
            )
            embed.set_image(url=image[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Wiki(client))
