import discord
from discord.ext import commands
from discord import Activity, ActivityType, AllowedMentions
from discord.ext.commands import when_mentioned_or
from modules.wiki import Wiki

import env_file
import logging

token = env_file.get()

logging.basicConfig(level=logging.INFO)

client = commands.Bot(
    command_prefix=when_mentioned_or("mc "),
    help_command=None,
    allowed_mentions=AllowedMentions.none(),
)


@client.event
async def on_ready():
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching, name="you getting all that experience."
        )
    )
    print(f'Bot is running as "{client.user}"')
    print("=========================================")


@client.command()
async def ping(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="Ping",
            colour=ctx.author.colour,
            description=f"Pong! `Latency: {round(client.latency * 1000)} ms`",
        )
    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.send(
        "https://discord.com/api/oauth2/authorize?client_id=784725037172129803&permissions=379968&scope=bot"
    )


client.add_cog(Wiki(client))

client.run(token["BOT_TOKEN"])