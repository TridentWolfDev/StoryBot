
# bot.py
import discord
import os
from dotenv import load_dotenv
import mysql.connector
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('channels.db')
cur = conn.cursor()

def findChannelInGuild(ctx):
    channels = cur.execute("select channel_id from channels").fetchall()
    id = discord.utils.find(lambda m: bot.get_channel(m[0]).guild == ctx.guild, channels)
    if id is None:
        return "Channel not assigned."
    return id[0]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AUTHOR = os.getenv('AUTHOR')

bot = commands.Bot(command_prefix='+')

storyList = []
story = ""

@bot.event
async def on_ready():
    print("Bot successfully connected.")

@bot.command(pass_context=True, help='Sets the channel for the One Word Story')
async def setChannel(ctx, channelId : int):
    if ctx.message.author == bot.user:
        return

    textChannels = []
    for c in ctx.guild.channels:
            textChannels.append(c.id)

    if channelId in textChannels and ctx.message.author.guild_permissions.administrator and type(findChannelInGuild(ctx)) == str:
        await ctx.send('Channel set successfully.')
        cur.execute("insert into channels values (?)", (channelId,))
    else:
        await ctx.send("""You do not have the permissions to set channel or the channel is invalid.
Make sure there isn't another channel set in this guild.""")

    conn.commit()

@bot.command(pass_context=True, help='Removes One Word Story from a channel')
async def rmChannel(ctx):
    if ctx.message.author == bot.user:
        return

    if ctx.message.author.guild_permissions.administrator and type(findChannelInGuild(ctx)) != str:
        cur.execute("delete from channels where channel_id = ?", (findChannelInGuild(ctx),))
        await ctx.send("Channel removed successfully")
    else:
        await ctx.send("You do not have the permissions to set channel or there is no channel set in this guild.")

@bot.command(pass_context=True, help='Sends the One Word Story channel ID')
async def getChannel(ctx):
    if ctx.message.author == bot.user:
        return 

    await ctx.send(findChannelInGuild(ctx))

@bot.command(pass_context=True, help='Sends the One Word Story')
async def getStory(ctx):
    if ctx.message.author == bot.user:
        return

    elif type(findChannelInGuild(ctx)) == str:
         await ctx.send("No channel assigned.")
         return

    storyList = []
    story = ""
    async for m in bot.get_channel(findChannelInGuild(ctx)).history(limit=200):
        storyList.append(m.content)
    for i in storyList[::-1]:
        story += i + ' '

    if len(story) > 2000:
        await ctx.send("Story too long.")
    else:
        await ctx.send(story)


bot.run(TOKEN)
