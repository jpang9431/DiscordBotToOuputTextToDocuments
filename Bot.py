import os
import datetime
import time
import discord
from discord import app_commands
from discord.ext import commands

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
token = ""
fullTextOutputFilePath = ""
sepicalTextOutputFilePath = ""
@client.event
async def on_ready():
    print("Online")
    synced = await client.tree.sync()
    print(len(synced))

@client.tree.command(name="getchannelids", description="Get all channel ids")
async def getChannelIds(interaction: discord.Interaction):
    await interaction.response.send_message("Started Process")
    guild = interaction.guild
    channels = guild.text_channels
    for channel in channels:
        await interaction.channel.send("#"+str(channel.id) + ","+channel.name)
    await interaction.channel.send("Done")

@client.tree.command(name="getroleids", description="Get role ids")
async def getRoleIds(interaction: discord.Interaction):
    await interaction.response.send_message("Started Process")
    guild = interaction.guild
    roles = guild.roles
    for role in roles:
        if (role.name!="@everyone"):
         await interaction.channel.send("@&"+str(role.id)+">"+","+role.name)
    await interaction.channel.send("Done")

@client.tree.command(name="getspecialcombinations", description="Get special escape discord characters")
async def getspecialcombinations(interaction: discord.Interaction):
    guild = interaction.guild
    filePath = sepicalTextOutputFilePath
    await interaction.response.send_message("Started")
    file = open(filePath, "w", encoding="utf-8")
    total = 0
    for role in guild.roles:
        if (role.name!="@everyone"):
            file.write("<@&"+str(role.id)+">"+","+"@"+role.name+"\n")
            total+=1
    await interaction.channel.send(str(total)+" roles found excluding everyone")
    lastTotal = total
    for channel in guild.channels:
        file.write("<#"+str(channel.id)+">"+","+"#"+channel.name+"\n")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" channels found")
    lastTotal = total
    for user in guild.members:
        file.write("<@"+str(user.id)+">"+","+"@"+user.name+"\n")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" members found")
    lastTotal = total
    for emoji in guild.emojis:
        file.write("<:"+str(emoji.name)+":"+str(emoji.id)+">,"+":"+emoji.name+":"+"\n")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" custom emjois found")
    file.close()

@client.tree.command(name = "outputtotxt", description="Parse through channel text to output it to console")
async def outputtotxt(interaction: discord.Interaction):
    guild = interaction.guild
    channels = guild.text_channels
    count = 0
    filepath = fullTextOutputFilePath
    file = open(filepath, "w", encoding="utf-8")
    await interaction.response.send_message("Started")
    totalTime = time.time()
    for channel in channels:
        messagesInChannel = 0
        now = time.time()
        async for msg in channel.history(limit=20000, oldest_first=True):
            if (msg.author.global_name!=None and msg.content!=""):
                item = str(msg.author.global_name) + "," + str(msg.content.replace("\n"," "))+"\n"
                file.write(item)
                count+=1
                messagesInChannel+=1
        now = time.time()-now
        await interaction.channel.send(str(messagesInChannel) + " messages by users outputted in "+channel.name+" | "+str(now))
    totalTime = time.time()-totalTime
    await interaction.channel.send(str(count) + " messages by users outputted | "+str(totalTime))
    file.close()
client.run(token)