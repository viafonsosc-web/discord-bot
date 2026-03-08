import discord
from discord.ext import commands
import json
import os
from flask import Flask
import threading

# ------------------------------
# Configurações iniciais
# ------------------------------
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
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

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
    valid_ranks = ['Iron','Bronze','Silver','Gold','Platinum','Diamond','Ascendant','Immortal','Radiant','SS','S','A','B','C']

    if rank not in valid_ranks:
        await ctx.send("❌ Rank inválido!")
        return

    players[name] = {
        'rank': rank,
        'bounty': players.get(name, {}).get('bounty', 0),
        'cla': players.get(name, {}).get('cla', 'Não definido'),
        'respiracao': players.get(name, {}).get('respiracao', 'Não definido'),
        'espada': players.get(name, {}).get('espada', 'Não definido'),
        'raca': players.get(name, {}).get('raca', 'Não definido'),
        'estilo': players.get(name, {}).get('estilo', 'Não definido'),
        'tempo': players.get(name, {}).get('tempo', 'Não definido')
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
# Comando !setinfo (ADMIN) — cadastra todos os dados
# ------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def setinfo(ctx, name: str, rank: str, bounty: int, cla: str, respiracao: str, espada: str, raca: str, estilo: str, tempo: str):
    players = load_players()
    valid_ranks = ['Iron','Bronze','Silver','Gold','Platinum','Diamond','Ascendant','Immortal','Radiant','SS','S','A','B','C']

    if rank not in valid_ranks:
        await ctx.send("❌ Rank inválido!")
        return

    if bounty > 10000:
        bounty = 10000

    players[name] = {
        'rank': rank,
        'bounty': bounty,
        'cla': cla,
        'respiracao': respiracao,
        'espada': espada,
        'raca': raca,
        'estilo': estilo,
        'tempo': tempo
    }

    save_players(players)

    embed = discord.Embed(
        title="✨ Player Registrado/Atualizado!",
        color=0x8A2BE2
    )
    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=rank, inline=False)
    embed.add_field(name="💰 Bounty", value=bounty, inline=False)
    embed.add_field(name="⚔️ Cla Principal", value=cla, inline=False)
    embed.add_field(name="💨 Respiração atual", value=respiracao, inline=False)
    embed.add_field(name="🗡️ Espada", value=espada, inline=False)
    embed.add_field(name="🧬 Raça", value=raca, inline=False)
    embed.add_field(name="🎮 Estilo de Jogo", value=estilo, inline=False)
    embed.add_field(name="⏱️ Tempo Estimado Jogando", value=tempo, inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !info (TODOS)
# ------------------------------
@bot.command()
async def info(ctx, name: str):
    players = load_players()

    if name not in players:
        await ctx.send("❌ Player não registrado!")
        return

    data = players[name]
    embed = discord.Embed(
        title=f"📋 Informações de {name}",
        color=0x8A2BE2
    )
    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=data.get('rank', 'Não definido'), inline=False)
    embed.add_field(name="💰 Bounty", value=data.get('bounty', 0), inline=False)
    embed.add_field(name="⚔️ Cla Principal", value=data.get('cla', 'Não definido'), inline=False)
    embed.add_field(name="💨 Respiração Principal", value=data.get('respiracao', 'Não definido'), inline=False)
    embed.add_field(name="🗡️ Espada", value=data.get('espada', 'Não definido'), inline=False)
    embed.add_field(name="🧬 Raça", value=data.get('raca', 'Não definido'), inline=False)
    embed.add_field(name="🎮 Estilo de Jogo", value=data.get('estilo', 'Não definido'), inline=False)
    embed.add_field(name="⏱️ Tempo Estimado Jogando", value=data.get('tempo', 'Não definido'), inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !profile (TODOS) — mantém funcional
# ------------------------------
@bot.command()
async def profile(ctx, name: str):
    players = load_players()

    if name not in players:
        await ctx.send("❌ Player não registrado!")
        return

    data = players[name]
    embed = discord.Embed(
        title="📜 Perfil do Player",
        color=0x8A2BE2
    )
    embed.add_field(name="🧑 Nome", value=name, inline=False)
    embed.add_field(name="🏆 Rank", value=data.get('rank', 'Não definido'), inline=False)
    embed.add_field(name="💰 Bounty", value=data.get('bounty', 0), inline=False)

    await ctx.send(embed=embed)

# ------------------------------
# Comando !players (TODOS)
# ------------------------------
@bot.command()
async def players(ctx):
    players_data = load_players()

    if not players_data:
        await ctx.send("❌ Nenhum player registrado ainda.")
        return

    text = ""
    for name, data in players_data.items():
        text += f"🧑 {name} — 🏆 {data.get('rank','Não definido')} — 💰 {data.get('bounty',0)}\n"

    embed = discord.Embed(
        title="📋 Lista de Players",
        description=text,
        color=0x8A2BE2
    )

    await ctx.send(embed=embed)

# ------------------------------
# Comando !top (TODOS)
# ------------------------------
@bot.command()
async def top(ctx):
    players = load_players()

    if not players:
        await ctx.send("❌ Nenhum player registrado.")
        return

    ranking = sorted(players.items(), key=lambda x: x[1].get('bounty', 0), reverse=True)

    embed = discord.Embed(
        title="🏆 Top 10 Players por Bounty",
        color=0x8A2BE2
    )

    text = ""
    for pos, (name, data) in enumerate(ranking[:10], start=1):
        text += f"**{pos}. {name}** — 🏆 {data.get('rank','Não definido')} — 💰 {data.get('bounty',0)}\n"

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
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando não encontrado.")
    else:
        print(error)

# ------------------------------
# Servidor HTTP mínimo para Render (opcional)
# ------------------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot Khonsu está online!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Rodar Flask em thread separada
threading.Thread(target=run_flask).start()

# ------------------------------
# Rodar o bot
# ------------------------------
bot.run(os.getenv("DISCORD_TOKEN"))



