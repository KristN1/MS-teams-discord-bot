import pymsteams
import discord
from discord.ext import commands

client = commands.Bot(command_prefix=".")
prefix = (".")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def teams(ctx):
    teams = pymsteams.connectorcard("WEBHOOK_LINK")

#Message title
    await ctx.send("Please set message title.")
    title = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)

#Message colour
    await ctx.send("Please set colour HEX, type `skip` to ignore.")
    colour = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)

#Link title
    await ctx.send("Please set link title, type `skip` to ignore.")
    linktitle = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)
    if linktitle.content != "skip":
#link
        await ctx.send("Please set link.")
        link = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)

#Message content
    await ctx.send("Please set message content.")
    msg = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)


# - - - EMBED - - -
#Sets embed title
    embed=discord.Embed(title="MS Teams message", color=0x4F58CA)

#Sets title
    embed.add_field(name="Title:", value=f"{title.content}", inline=False)
    teams.title(title.content)

#Sets colour and if it is defined
    embed_colour = colour.content
    if colour.content == "skip":
        embed_colour = "Not defined"
    embed.add_field(name="Colour:", value=f"{embed_colour}", inline=False)
    teams.color(colour.content)

#Sets link title and if it has been skipped
    if linktitle.content != "skip" and link.content != "skip":
        embed.add_field(name="Link title:", value=f"{linktitle.content}", inline=False)
        embed.add_field(name="Link:", value=f"{link.content}", inline=False)
        teams.addLinkButton(linktitle.content, link.content)

#Sets message content
    embed.add_field(name="Message content:", value=f"{msg.content}", inline=False)
    teams.text(msg.content)

#Sets embed footed and sends embed
    embed.set_footer(text=f"Message sent by {ctx.author.name}")
    await ctx.send(embed=embed)

#Requests final user confirmation
    await ctx.send("Type **y** to confirm and **n** to cancel")
    confirm = await client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id)
    if confirm.content == "y":
        teams.send()
        await ctx.send("message sent")
    elif confirm.content == "n":
        await ctx.send("canceled")

client.run("BOT_TOKEN")