import os
import datetime
import discord

client = discord.Client()


def update_mc():
    dtstr = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    ).strftime("%y-%m-%d %H:%M:%S")
    guild = client.get_guild(os.getenv("GUILD_ID"))
    member_role = guild.get_role(os.getenv("ROLE_ID"))
    mc = sum(1 for member in member_role.members if not member.bot)
    print(f"[{dtstr}] {mc} members has member role")
    channel = client.get_channel(os.getenv("CHANNEL_ID"))
    err = False
    try:
        channel.edit(name="メンバー数: {mc}")
    except Exception as e:
        print(e)
        err = True
    return mc, err


@client.event
async def on_raw_reaction_add(p):
    update_mc()


@client.event
async def on_raw_reaction_remove(p):
    update_mc()


@client.event
async def on_raw_reaction_clear_emoji(p):
    update_mc()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.strip() == "sb!count":
        mc, err = update_mc()
        await message.channel.send(f"現在のメンバー数は {mc} です。")
        if err:
            await message.channel.send("チャンネル名を変更できませんでした。")


client.run(os.getenv("TOKEN"))
