import discord
from discord.ext import commands
import requests
import time
import datetime
import random
from modules import scrape


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    def username_to_uuid(self, username: str):
        ts = time.time()
        response = requests.get(
            f"https://api.mojang.com/users/profiles/minecraft/{username}?at={str(ts)}"
        ).json()
        uuid = response["id"]
        return uuid

    def name_history(self, uuid: str):
        response = requests.get(
            f"https://api.mojang.com/user/profiles/{uuid}/names"
        ).json()
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
            embed.add_field(
                name="Skin",
                inline=False,
                value=f"[Render](https://mc-heads.net/body/{uuid}) | [Download](https://mc-heads.net/download/{uuid})",
            )
            name_history = ""
            count = 1
            for names in history:
                try:
                    name = names["name"]
                    timestamp = names["changedToAt"]
                except KeyError:
                    timestamp = "-"
                if timestamp != "-":
                    date = datetime.datetime.fromtimestamp(timestamp / 1000.0)
                else:
                    date = "Original Username"
                name_history += f"**{count}.** `{name}`: `{date}`\n"
                count += 1
            embed.add_field(name="Name History", inline=False, value=name_history)
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{uuid}.png/left")
            # embed.set_footer(text=f"Tip:\n{random.choice(scrape.tips_tricks())}")
        await ctx.send(embed=embed)

    def get_server_info(self, hostname: str):
        server_response = requests.get(f"https://api.mcsrvstat.us/2/{hostname}").json()
        try:
            description = server_response["motd"]["clean"]
            motd = ""
            for items in description:
                motd += f"{items}\n"
        except KeyError:
            motd = "None"
        try:
            online_players = server_response["players"]["online"]
        except KeyError:
            online_players = "None"
        try:
            max_players = server_response["players"]["max"]
        except KeyError:
            max_players = "None"
        try:
            version = server_response["version"]
        except KeyError:
            version = "None"
        online = server_response["online"]
        if not online:
            online = "Offline"
        else:
            online = "Online"
        try:
            software = server_response["software"]
        except KeyError:
            software = "None"
        return motd, online_players, max_players, version, online, software

    @commands.command(aliases=["server"])
    async def serverinfo(self, ctx, *, server_ip: str):
        async with ctx.channel.typing():
            (
                description,
                online_players,
                max_players,
                version,
                online,
                software,
            ) = self.get_server_info(server_ip)
            embed = discord.Embed(
                title=server_ip,
                colour=ctx.author.colour,
                description=description,
            )
            embed.add_field(name="Status", value=f"{online}")
            embed.add_field(name="Max Players", value=f"{max_players}")
            embed.add_field(name="Online Players", value=f"{online_players}")
            embed.add_field(name="Version", value=f"{version}")
            embed.add_field(name="Software", value=f"{software}")
            embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{server_ip}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Profile(client))
