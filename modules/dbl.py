import topgg
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client

        self.dbl_token = os.getenv("DBL_TOKEN")  # set this to your bot's Top.gg token

        self.client.topggpy = topgg.DBLClient(
            client, self.dbl_token, autopost=True, post_shard_count=True
        )

    @commands.Cog.listener()
    async def on_autopost_success(self):
        print(
            f"Posted server count ({self.client.topggpy.guild_count}), shard count ({self.client.shard_count})"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("BFD_TOKEN"),
        }
        data = {"server_count": len(self.client.guilds)}
        response = requests.post(
            "https://discords.com/bots/api/bot/784725037172129803",
            json=data,
            headers=headers,
        )
        print("Server count posted successfully on discords.com")


def setup(client):
    client.add_cog(TopGG(client))
