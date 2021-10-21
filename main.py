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
async def explain(ctx, *, arg):
    code = await depyify(arg)
    explanation = OpenAI.explain(code)
    await ctx.send(f"`{explanation}`")


@client.command()
async def code(ctx, *, arg):
    code = OpenAI.code(arg)
    code = await pyify(code)
    await ctx.send(f"{code}")


if __name__ == "__main__":
    client.run(BOT_TOKEN)
