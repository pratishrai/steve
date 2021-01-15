import discord
from discord.ext import commands
import requests
import time
import datetime


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    def username_to_uuid(self, username: str):
        ts = time.time()
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?at={str(ts)}").json()
        uuid = response["id"]
        return uuid

    def name_history(self, uuid: str):
        response = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
        return response

    @commands.command()
    async def profile(self, ctx, username: str):
        async with ctx.channel.typing():
            uuid = self.username_to_uuid(username=username)
            history = self.name_history(uuid)
            embed = discord.Embed(
                title=f"{history[-1]['name']}'s profile",
                colour=ctx.author.colour,
            )
            embed.add_field(name="UUID", inline=False, value=f"`{uuid}`")
            name_history = ""
            count = 1
            for names in history:
                try:
                    name = names["name"]
                    timestamp = names["changedToAt"]
                except KeyError:
                    timestamp = "-"
                if timestamp != "-":
                    date = datetime.datetime.fromtimestamp(timestamp/1000.0)
                else:
                    date = "Original Username"
                name_history += f"**{count}.** {name}: `{date}`\n"
                count += 1
            embed.add_field(name="Name History", inline=False, value=name_history)
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{uuid}.png")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Profile(client))
