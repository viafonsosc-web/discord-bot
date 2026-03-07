import discord
from discord.ext import commands
import json
import os

# Configurações iniciais
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'players.json'

# ------------------------------
# Funções para salvar e carregar
# ------------------------------
def load_players():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_players(players):
    with open(DATA_FILE, 'w') as f:
        json.dump(players, f, indent=4)

# ------------------------------
# Comando !setrank (ADMIN)
# ------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def setrank(ctx, name: str, rank: str):

    players = load_players()

    valid_ranks = ['Iron','Bronze','Silver','Gold','Platinum','Diamond','Ascendant','Immortal','Radiant','SS']

    if rank not in valid_ranks:
        await ctx.send("❌ Rank inválido!")
        return

    players[name] = {
        'rank': rank,
        'bounty': players.get(name, {}).get('bounty', 0)
    }

    save_players(players)

    embed = discord.Embed(
        title="✨ Player Registrado!",
        color=0x8A2BE2
    )

    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=rank, inline=False)
    embed.add_field(name="💰 Bounty", value=players[name]['bounty'], inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !bounty (ADMIN)
# ------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def bounty(ctx, name: str, value: int):

    players = load_players()

    if name not in players:
        await ctx.send("❌ Player não registrado!")
        return

    if value > 10000:
        value = 10000

    players[name]['bounty'] = value
    save_players(players)

    embed = discord.Embed(
        title="💰 Bounty Atualizada!",
        color=0x8A2BE2
    )

    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=players[name]['rank'], inline=False)
    embed.add_field(name="💵 Nova Bounty", value=value, inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !profile (TODOS)
# ------------------------------
@bot.command()
async def profile(ctx, name: str):

    players = load_players()

    if name not in players:
        await ctx.send("❌ Player não registrado!")
        return

    embed = discord.Embed(
        title="📜 Perfil do Player",
        color=0x8A2BE2
    )

    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=players[name]['rank'], inline=False)
    embed.add_field(name="💰 Bounty", value=players[name]['bounty'], inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !top (ranking)
# ------------------------------
@bot.command()
async def top(ctx):

    players = load_players()

    if not players:
        await ctx.send("Nenhum player registrado.")
        return

    ranking = sorted(players.items(), key=lambda x: x[1]['bounty'], reverse=True)

    embed = discord.Embed(
        title="🏆 Ranking de Bounty",
        color=0x8A2BE2
    )

    pos = 1
    text = ""

    for name, data in ranking[:10]:
        text += f"**{pos}. {name}** — 💰 {data['bounty']}\n"
        pos += 1

    embed.description = text

    await ctx.send(embed=embed)

# ------------------------------
# Comando !remover (ADMIN)
# ------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def remover(ctx, name: str):

    players = load_players()

    if name not in players:
        await ctx.send("❌ Player não existe.")
        return

    del players[name]

    save_players(players)

    await ctx.send(f"🗑️ Player **{name}** removido.")

# ------------------------------
# Erro de permissão
# ------------------------------
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Apenas **administradores** podem usar esse comando.")

# ------------------------------
# Rodar o bot
# ------------------------------
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

# Pega o token da variável de ambiente
bot.run(os.getenv("MTQ3OTg2OTkzNjkzNDQ1NzU2NQ.G2Or_d.XYUz8dNRj_VnUdnzZfaJ3PxvxDTeqss5empdoU"))


