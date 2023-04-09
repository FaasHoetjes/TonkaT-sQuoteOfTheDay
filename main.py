import discord
import os
import requests
import asyncio
import random
from dotenv import load_dotenv


load_dotenv()
client = discord.Client(intents=discord.Intents.default())
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
streamer_name = "loltyler1"

print(
    "Client ID: "
    + client_id
    + "\nClient Secret: "
    + client_secret
    + "\nStreamer Name: "
    + streamer_name
)


body = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials",
}


response = requests.post("https://id.twitch.tv/oauth2/token", body)
keys = response.json()
headers = {"Client-ID": client_id, "Authorization": f"Bearer {keys['access_token']}"}


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = discord.utils.get(client.get_all_channels(), name="hackermen")
    is_live = False

    while True:
        random_number = random.randint(1, 10000)
        print("Random number is: " + str(random_number))
        stream = requests.get(
            f"https://api.twitch.tv/helix/streams?user_login={streamer_name}",
            headers=headers,
        )
        stream_data = stream.json()
        if len(stream_data["data"]) == 1 and not is_live:
            print("Stream is live")
            is_live = True
            await channel.send(stream_data["data"][0]["title"])
        elif len(stream_data["data"]) == 0 and is_live:
            print("Stream is offline")
            is_live = False
        elif random_number == 1:
            await channel.send("DOPA DOWNNN!")
        await asyncio.sleep(60)


client.run(os.getenv("DISCORD_TOKEN"))
