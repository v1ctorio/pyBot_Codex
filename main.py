import os
import discord
from discord.ext import commands
import OpenAI


BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PREFIX = "py "
client = commands.Bot(command_prefix=PREFIX, activity=discord.Game(name=f"{PREFIX}help"))
client.remove_command("help")


async def pyify(code):
    return f"```py\n{code}```"


async def depyify(code):
    return code.replace("```py\n", "").replace("```", "")


@client.event
async def on_ready():
    print("Bot has successfully logged in as: {}".format(client.user))
    print("Bot ID: {}\n".format(client.user.id))


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="List of commands",
        color=discord.Colour.from_rgb(225, 224, 120)

    )
    embed.add_field(
        name="**py ask**",
        value="Ask any python related question.\n" \
              "Ex. `py ask How do I use regex?`",
        inline=False
    )
    embed.add_field(
        name="**py code**",
        value="pyBot will code following your instructions\n" \
              "Ex. `py code\n1. import random\n2. Print a random number between 1 and 100`",
        inline=False
    )
    explain_example_code = \
        r"""word = input()
output = ""
first_vowel = True
for char in word:
    if char in "aeiou" and first_vowel:
        char *= 10
        first_vowel = False
    output += char

print(output)
"""
    embed.add_field(
        name="**ger explain**",
        value="pyBot will explain the piece of code you ask\n" \
              f"Ex.`py explain` {await pyify(explain_example_code)}",
        inline=False
    )
    embed.set_footer(
        text="Warning: this bot is still being developed and you may encounter errors"
    )
    emoji = "\u2705"
    await ctx.message.add_reaction(emoji)
    await ctx.author.send(embed=embed)


@client.command()
async def explain(ctx, *, arg):
    print(ctx.message.author)
    async with ctx.typing():
        code = await depyify(arg)
        explanation = OpenAI.explain(code)
        await ctx.send(f"**Here is what the code above is doing:**`{explanation}`")


@client.command()
async def code(ctx, *, arg):
    print(ctx.message.author)
    async with ctx.typing():
        code = OpenAI.code(arg)
        code = await pyify(code)
        await ctx.send(f"**You can do that by following the code below:**\n{code}")


@client.command()
async def ask(ctx, *, question):
    print(ctx.message.author)
    async with ctx.typing():
        answer = OpenAI.ask(question)
        await ctx.send(f"{answer}")


if __name__ == "__main__":
    client.run(BOT_TOKEN)
