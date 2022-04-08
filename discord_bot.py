import os
import datetime
import discord

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


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
