import dbl
import discord
from discord.ext import commands
import env_file
import requests

token = env_file.get()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client
        self.token = token["DBL_TOKEN"]
        self.dblpy = dbl.DBLClient(
            self.client, self.token, autopost=True
        )  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully on top.gg")
        headers = {
            "Content-Type": "application/json",
            "Authorization": token["BFD_TOKEN"],
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
