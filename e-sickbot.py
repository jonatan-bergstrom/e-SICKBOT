#!/usr/bin/python
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from datetime import *
import random
import wolframalpha
import keys

bot = commands.Bot(command_prefix='!')
svar = ["Ja", "Nej", "Definitivt", "Troligen", "Absolut", "Absolut inte", "Käften", "Garanterat", "Väldigt tveksamt"]

wolfram = wolframalpha.Client(keys.wolfram)
stored_answer = ""


@bot.command()
async def hello(ctx):
    if ctx.message.author.nick:
        await ctx.send("Käften {}!".format(ctx.message.author.nick))
    else:
        await ctx.send("Käften {}!".format(ctx.message.author.name))
        
        
@bot.command(name='hype',
    aliases=['hostlan','höstlan'])
async def hype(ctx):
    today = date.today()
    future = date(2020,10,10)
    until = str((future - today).days)
    await ctx.send("{} days until e-SICK hÖSTLAN!".format(until))
    
    
@bot.command(name="fact")
async def fact(ctx):
    await ctx.send(random.choice(facts.factlist))
    
    
@bot.command(name='choose',
    aliases=['välj'])
async def choose(ctx):
    if "eller" in ctx.message.content:
        c_svar = ["såklart!", "tror jag", "alla gånger!", "skulle jag ha valt"]
        msg = ctx.message.content.replace("!välj","").replace("!choose","")
        val = random.choice(msg.split("eller"))
        await ctx.send(val.strip() + " " + random.choice(c_svar))
    else:
        await ctx.send('Skriv "eller" mellan alternativen')
        
        
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    
@bot.event
async def on_message(message):
    if message.content.startswith("!wolf") or message.content.startswith("!wolfram"):
        msg = message.content.replace("!wolfram","").replace("!wolf","")
        res = wolfram.query(msg)
        if res['@success'] == 'false':
            await message.channel.send("Question cannot be resolved")
            print('Question cannot be resolved')
        # Wolfram was able to resolve question
        else:
            w_input = "Input: " + res["pod"][0]["subpod"]["plaintext"]
            result = "Result: " + res["pod"][1]["subpod"]["plaintext"]
            await message.channel.send(w_input)
            for r in result.split("\n"):
                await message.channel.send(r)  
    elif message.content.startswith("!st ") or message.content.startswith("!st "):
        global stored_answer
        stored_answer =  message.content.replace("!st ", "").replace("!store ", "")
    elif bot.user.mentioned_in(message) and message.mention_everyone is False:
        if message.content.lower()[-1] == "?":
            if stored_answer == "":
                if random.random() < 0.15:
                    for i in range(100):
                        u = random.choice(message.channel.guild.members)
                        if u !=  message.author:
                            break
                            print(u.nick)
                    if u.nick:
                        m = "Vet inte, fråga {}".format(u.nick)
                    else:
                        m = "Vet inte, fråga {}".format(u.name)
                    await message.channel.send(m)
                else:
                    await message.channel.send(random.choice(svar))
            else:
                await message.channel.send(stored_answer)
                global stored_answer
                stored_answer = ""
    else:
        await bot.process_commands(message)
        
        
@bot.event
async def on_voice_state_update(member,before, after):
        if after.channel != None:
                for channel in after.channel.guild.channels:
                        if channel.name == "allmänt-ez" or channel.name == "chatta":
                                await channel.send("{} joined voice channel {}".format(member.name,after.channel.name))
                                
                                
bot.run(keys.discord)
