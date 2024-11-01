import os
import datetime
import time
import discord
from discord import app_commands
from discord.ext import commands
import json

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

secertFile = open("config.json")
fileData = json.load(secertFile)

token = fileData["token"]
fullTextOutputFilePath = fileData["fullTextOutputFilePath"]
sepicalTextOutputFilePath = fileData["sepicalTextOutputFilePath"]

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

async def getSpeicalCombinations(interaction: discord.Interaction, speicalEscapes, regularReplace,typeOfEscape):
    guild = interaction.guild
    filePath = sepicalTextOutputFilePath
    await interaction.response.send_message("Started")
    file = open(filePath, "w", encoding="utf-8")
    total = 0
    for role in guild.roles:
        speicalEscapes.append("<@&"+str(role.id)+">")
        regularReplace.append("@"+role.name)
        typeOfEscape.append("Role Ping")
        total+=1
    await interaction.channel.send(str(total)+" roles found excluding everyone")
    lastTotal = total
    for channel in guild.channels:
        speicalEscapes.append("<#"+str(channel.id)+">")
        regularReplace.append("#"+channel.name)
        typeOfEscape.append("Channel Mention")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" channels found")
    lastTotal = total
    for user in guild.members:
        speicalEscapes.append("<@"+str(user.id)+">")
        regularReplace.append("@"+user.display_name)
        typeOfEscape.append("User Ping")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" members found")
    lastTotal = total
    for emoji in guild.emojis:
        speicalEscapes.append("<:"+str(emoji.name)+":"+str(emoji.id)+">")
        regularReplace.append(":"+emoji.name+":")
        typeOfEscape.append("Emjoi Use")
        total+=1
    await interaction.channel.send(str(total-lastTotal)+" custom emjois found")
    for i in range(len(speicalEscapes)):
        file.write(speicalEscapes[i]+","+regularReplace[i]+","+typeOfEscape[i]+"\n")
    file.close()    
    
@client.tree.command(name="getspecialcombinations", description="Get special escape discord characters")
async def getspecialcombinations(interaction: discord.Interaction):
    speicalEscapes = []
    regularReplace = []
    typeOfEscape = []
    await getSpeicalCombinations(interaction, speicalEscapes, regularReplace, typeOfEscape)

@client.tree.command(name = "outputtotxt", description="Parse through channel text to output it to console")
async def outputtotxt(interaction: discord.Interaction):
    guild = interaction.guild
    speicalEscapes = []
    regularReplace = []
    typeOfEscape = []
    await getSpeicalCombinations(interaction, speicalEscapes, regularReplace, typeOfEscape)
    channels = guild.text_channels
    count = 0
    filepath = fullTextOutputFilePath
    file = open(filepath, "w", encoding="utf-8")
    totalTime = time.time()
    for channel in channels:
        messagesInChannel = 0
        now = time.time()
        async for msg in channel.history(limit=2000000, oldest_first=True):
            if (msg.author.global_name!=None and msg.content!=""):
                strContent = msg.content.replace("\n"," ")
                for i in range(len(speicalEscapes)):
                    strContent = strContent.replace(speicalEscapes[i],regularReplace[i])
                item = str(msg.author.global_name) + "," + str(strContent)+"\n"
                file.write(item)
                count+=1
                messagesInChannel+=1
        now = time.time()-now
        await interaction.channel.send(str(messagesInChannel) + " messages by users outputted in "+channel.name+" | "+str(now))
    totalTime = time.time()-totalTime
    await interaction.channel.send(str(count) + " messages by users outputted | "+str(totalTime))
    file.close()
    
client.run(token)