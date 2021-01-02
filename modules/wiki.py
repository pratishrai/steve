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
            description = f"{about[0]}"
            if len(about) > 3:
                description = f"{about[0]}\n{about[1]}\n{about[2]}"

            embed = discord.Embed(
                title=f"{title[0]}",
                colour=ctx.author.colour,
                description=description,
            )
            embed.set_image(url=image[0])
        await ctx.send(embed=embed)

    @commands.command()
    async def wiki(self, ctx, *, query: str):
        async with ctx.channel.typing():
            url = scrape.search(query=query)
        await ctx.send(f"{url}")

    @commands.command()
    async def table(self, ctx, *, query: str):
        async with ctx.channel.typing():
            url = scrape.search(query=query)
            title, table, image = scrape.scrape_table(url=url)
            image = image.split("/revision")
            title = title.split("–")
            description = str(table)

            embed = discord.Embed(
                title=f"{title[0]}", colour=ctx.author.colour, description=description
            )
            embed.set_thumbnail(url=image[0])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Wiki(client))
