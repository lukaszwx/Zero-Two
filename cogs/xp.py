import discord
from discord.ext import commands
from discord import app_commands
import json
import os

XP_FILE = "xp_data.json"

def load_xp():
    if not os.path.exists(XP_FILE):
        return {}
    with open(XP_FILE, "r") as f:
        return json.load(f)

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f)

def add_xp(user_id, amount=5):
    data = load_xp()
    user_id = str(user_id)
    data[user_id] = data.get(user_id, 0) + amount
    save_xp(data)
    return data[user_id]

def get_xp(user_id):
    data = load_xp()
    return data.get(str(user_id), 0)

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        add_xp(message.author.id, 5)  # 5 XP por mensagem

    # Estes comandos são só métodos, não comandos slash ainda!
    async def xp(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        xp = get_xp(user.id)
        await interaction.response.send_message(f"{user.mention} tem **{xp} XP!**🆙", ephemeral=True)

    async def rank(self, interaction: discord.Interaction):
        data = load_xp()
        sorted_xp = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
        msg = "**Top 10 XP**\n\n"
        for i, (uid, xp) in enumerate(sorted_xp, 1):
            try:
                user = await self.bot.fetch_user(int(uid))
                user_display = user.mention
            except:
                user_display = f"ID {uid}"
            msg += f"{i}. {user_display} - {xp} XP\n"
        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    cog = XP(bot)
    await bot.add_cog(cog)
    # Agora sim, registra os comandos slash na árvore!
    bot.tree.add_command(app_commands.Command(
        name="xp",
        description="Veja seu XP atual.",
        callback=cog.xp,
        # Opcional: se quiser para guild específica, use guild=discord.Object(id=...),
    ))
    bot.tree.add_command(app_commands.Command(
        name="rank",
        description="Veja o ranking de XP do servidor.",
        callback=cog.rank,
    ))