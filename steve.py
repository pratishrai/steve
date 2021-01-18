import logging

import discord
import env_file
from discord import Activity, ActivityType, AllowedMentions
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from modules.profile import Profile
from modules.stats import Stats
from modules.wiki import Wiki
from modules.dbl import TopGG
from modules.rcon import Rcon

token = env_file.get()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.members = True

client = commands.Bot(
    command_prefix=when_mentioned_or("mc "),
    help_command=None,
    allowed_mentions=AllowedMentions.none(),
    intents=intents,
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


@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(
        colour=0x2859B8,
        description="""Hello, Thanks for adding Steve✨
        Steve is a simple and easy to use Discord bot that knows everything about Minecraft. About blocks, items, mobs, recipes, and even players!!
        Simply use the help command (`mc help`) to get started!""",
    )
    embed.add_field(
        name="**__Usefull Links__**",
        inline=False,
        value="""
    Check out Steve✨'s [Top.gg page](https://top.gg/bot/784725037172129803) for all features.
    Consider upvoting **[Steve✨](https://top.gg/bot/784725037172129803/vote)** on Top.gg
    Have an issue/suggestion? Join the **[Support Server](https://discord.gg/dKVfhV2jfn)**
    """,
    )
    await channel.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    await ctx.message.add_reaction("❌")
    print(error)


@client.command()
async def help(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="Help",
            colour=ctx.author.colour,
            description="Here is a list of commands you can use:",
        )
        embed.add_field(
            name="Info",
            inline=False,
            value=f"`{ctx.prefix}about <entity>` - Get Info about anything in Minecraft.\n`{ctx.prefix}wiki <entity>` "
            f"- Get the link to official wiki page of that entity.\n`{ctx.prefix}craft <item>` - Get the "
            f"crafting recipe for any item.\n`{ctx.prefix}profile <player>` - Get the Minecraft profile of any "
            f"player.",
        )
        embed.add_field(
            name="Developer",
            inline=False,
            value=f"`{ctx.prefix}stats` - Some statistics about the bot.",
        )
        embed.add_field(
            name="\u200b", inline=False, value="More commands coming soon..."
        )
    await ctx.send(embed=embed)


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
client.add_cog(Profile(client))
client.add_cog(Stats(client))
client.add_cog(TopGG(client))
client.add_cog(Rcon(client))

client.run(token["BOT_TOKEN"])
