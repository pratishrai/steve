import dbl
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client
        self.token = os.getenv("DBL_TOKEN")
        self.dblpy = dbl.DBLClient(
            self.client, self.token, autopost=True
        )  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully on top.gg")
        headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("BFD_TOKEN"),
        }
        data = {"server_count": len(self.client.guilds)}
        response = requests.post(
            "https://botsfordiscord.com/api/bot/784725037172129803",
            json=data,
            headers=headers,
        )
        print("Server count posted successfully on botsfordiscord.com")


def setup(client):
    client.add_cog(TopGG(client))
