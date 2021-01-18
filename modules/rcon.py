import discord
from discord.ext import commands

from modules.async_mcrcon import MinecraftClient


class Rcon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rcon(self, ctx, *, command: str):
        async with MinecraftClient("megumin.sed.lol", port, "aaaaaaaaaaa") as mc:
            output = await mc.send(f"{command}")
            await ctx.send(output)


def setup(client):
    client.add_cog(Rcon(client))
