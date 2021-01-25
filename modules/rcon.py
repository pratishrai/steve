import discord
from discord.ext import commands

from modules.async_mcrcon import MinecraftClient
from asyncio import TimeoutError

from database import RconCreds, add_creds, get_creds


class Rcon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rcon(self, ctx, *, command: str):
        if ctx.author == self.client.user:
            return

        user_host, user_port, user_password = get_creds(ctx.author.id)

        if user_host or user_port or user_password is not None:
            async with ctx.channel.typing():
                async with MinecraftClient(
                    f"{user_host}", int(user_port), f"{user_password}"
                ) as mc:
                    output = await mc.send(f"{command}")
            return await ctx.send(output)

        else:

            def check(m):
                return (
                    m.author == ctx.author
                    and m.channel.type == discord.ChannelType.private
                )

            try:
                await ctx.author.send("Please enter server address.")
                user_host = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except TimeoutError:
                await ctx.send("Timed-out, please run the command again.")
            try:
                await ctx.author.send("Please enter port.")
                user_port = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except TimeoutError:
                await ctx.send("Timed-out, please run the command again.")
            try:
                await ctx.author.send("Please enter password.")
                user_password = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except TimeoutError:
                await ctx.send("Timed-out, please run the command again.")

            async with ctx.channel.typing():
                async with MinecraftClient(
                    f"{user_host.content}",
                    int(user_port.content),
                    f"{user_password.content}",
                ) as mc:
                    output = await mc.send(f"{command}")
            await ctx.author.send(output)

            try:
                await ctx.author.send(
                    "Would you like to store these credentials for future use? [yes/no]"
                )
                answer = await self.client.wait_for(
                    "message", timeout=60.0, check=check
                )
            except TimeoutError:
                await ctx.send("Your credentials have not been stored.")
            if answer.content.lower() == "yes":
                creds = RconCreds(
                    member_id=ctx.author.id,
                    host=user_host.content,
                    port=int(user_port.content),
                    password=user_password.content,
                )
                add_creds(creds)
                await ctx.send(
                    "Okay, your credentials have been stored for future use."
                )
                print(f"{ctx.author}({ctx.author.id}) has stored their credentials")
            else:
                await ctx.send("Okay, your credentials will not been stored.")


def setup(client):
    client.add_cog(Rcon(client))
