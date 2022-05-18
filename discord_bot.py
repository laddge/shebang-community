import os
import time
import datetime
import threading
import discord
import tweepy

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def tweet():
    CK = os.getenv("TW_CK")
    CS = os.getenv("TW_CS")
    AT = os.getenv("TW_AT")
    AS = os.getenv("TW_AS")
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    status = """プログラミングに興味はありませんか？
これから学習する人、知識を共有したい人などが集まれる場所があります。
初心者も大歓迎！みんなで一緒に楽しくプログラミングしましょう！
現在の{}
#プログラミング #Shebang
https://shebang.laddge.net/"""
    while True:
        channel = client.get_channel(int(os.getenv("CHANNEL_ID")))
        if not channel:
            print("channel not found")
            time.sleep(1)
            continue
        api.update_status(status.format(channel.name))
        time.sleep(15000)


threading.Thread(target=tweet).start()


async def update_mc():
    dtstr = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    ).strftime("%y-%m-%d %H:%M:%S")
    guild = client.get_guild(int(os.getenv("GUILD_ID")))
    member_role = guild.get_role(int(os.getenv("ROLE_ID")))
    mc = sum(1 for member in member_role.members if not member.bot)
    print(f"[{dtstr}] {mc} members has member role")
    channel = client.get_channel(int(os.getenv("CHANNEL_ID")))
    err = False
    try:
        await channel.edit(name=f"メンバー数: {mc}")
    except Exception as e:
        print(e)
        err = True
    return mc, err


@client.event
async def on_member_update(b, a):
    await update_mc()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.strip() == "sb!count":
        mc, err = await update_mc()
        await message.channel.send(f"現在のメンバー数は {mc} です。")
        if err:
            await message.channel.send("チャンネル名を変更できませんでした。")


client.run(os.getenv("TOKEN"))
