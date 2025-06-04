import discord
from discord.ext import commands
from discord import app_commands, ui
import re
import ast
import operator
import math
import logging
from datetime import datetime
import random
import json
import os

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

GUILD_ID = 1378054602955554836
guild = discord.Object(id=GUILD_ID)

# Funções XP
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

def eval_expr(expr):
    """
    Avalia expressão matemática de forma segura.
    Suporta +, -, *, /, **, //, %, (), fatorial (!), e combinações.
    """
    operadores = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
    }

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operadores[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operadores[type(node.op)](_eval(node.operand))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == 'fact' and len(node.args) == 1:
                return math.factorial(int(_eval(node.args[0])))
            else:
                raise ValueError(f"Função {func_name} não suportada.")
        else:
            raise ValueError("Expressão inválida ou não suportada.")

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

def parse_fatorial(expr):
    """
    Substitui todos os casos de X! ou (Y)! por fact(X) ou fact(Y) recursivamente.
    Suporta múltiplos fatoriais na mesma expressão.
    """
    pattern = r'(\d+|\([^\(\)]+\))!'
    last = None
    while expr != last:
        last = expr
        expr = re.sub(pattern, r'fact(\1)', expr)
    return expr

class AdminSelec(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Silenciar membro", description="Coloca um membro em timeout"),
            discord.SelectOption(label="Desmutar membro", description="Remove timeout de um membro"),
            discord.SelectOption(label="Banir membro", description="Bane um membro do server"),
            discord.SelectOption(label="Expulsar membro", description="Expulsa um membro do server"),
            discord.SelectOption(label="Anunciar", description="Faz um anúncio no canal"),
            discord.SelectOption(label="Limpar mensagens", description="Apaga mensagens do canal"),
        ]
        super().__init__(placeholder="Escolha uma função...", options=options, custom_id="admin_select")

    async def callback(self, interaction: discord.Interaction):
        escolha = self.values[0]
        respostas = {
            "Silenciar membro": "🔇 Membro silenciado!",
            "Desmutar membro": "🔊 Membro desmutado!",
            "Banir membro": "🚫 Membro banido!",
            "Expulsar membro": "👢 Membro expulso!",
            "Anunciar": "📢 Anúncio enviado!",
            "Limpar mensagens": "🧹 Mensagens limpas!"
        }
        resposta = respostas.get(escolha, "❓ Função desconhecida.")
        await interaction.response.send_message(resposta, ephemeral=True)
        logging.info(f"Admin: {interaction.user} escolheu {escolha}")

class AdminMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AdminSelec())

class CalculadoraModal(ui.Modal, title="Calculadora da Zero Two"):
    expressao = ui.TextInput(
        label="Digite a expressão",
        style=discord.TextStyle.short,
        placeholder="Exemplo: (3+2)! + 2**3 - 4//2",
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        expr = self.expressao.value.lower()
        expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\,\%\!\ ]', '', expr).replace(',', '.')
        expr = parse_fatorial(expr)
        try:
            resultado = eval_expr(expr)
            await interaction.response.send_message(f"Resultado de `{expr}`: **{resultado}**", ephemeral=True)
            logging.info(f"CalculadoraModal: {interaction.user} calculou {expr} = {resultado}")
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao calcular: {e}\nExemplo válido: `3! + 2**3 - 4//2`", ephemeral=True)
            logging.error(f"Erro ao calcular {expr}: {e}")

class FerramentasSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Calculadora', description='Faça cálculos diretamente aqui'),
            discord.SelectOption(label='Relógio', description='Mostra o horário atual'),
            discord.SelectOption(label='Motivação', description='Receba uma frase motivacional')
        ]
        super().__init__(placeholder='Escolha uma ferramenta...', options=options, custom_id='ferramentas_select')

        self.frases_motivacao = [
            "💪 Você é mais forte do que imagina! Continue!",
            "🌟 Nunca desista dos seus sonhos.",
            "🔥 Acredite no seu potencial e vá em frente!",
            "💡 Cada dia é uma nova oportunidade para melhorar.",
            "🚀 Você pode alcançar tudo que desejar com esforço.",
            "🌈 Mantenha a positividade e espalhe luz.",
            "✨ Seu esforço será recompensado, continue firme!"
        ]

    async def callback(self, interaction: discord.Interaction):
        escolha = self.values[0]
        logging.info(f"Ferramentas: {interaction.user} escolheu {escolha}")
        if escolha == 'Calculadora':
            await interaction.response.send_modal(CalculadoraModal())
        elif escolha == 'Relógio':
            agora = datetime.now().strftime("%H:%M:%S")
            await interaction.response.send_message(f'🕒 Agora são {agora}.', ephemeral=True)
        elif escolha == 'Motivação':
            frase = random.choice(self.frases_motivacao)
            await interaction.response.send_message(frase, ephemeral=True)

class FerramentasMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FerramentasSelect())

class Gerais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # XP: ganha XP ao enviar mensagens
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        add_xp(message.author.id, 5)  # Dá XP a cada mensagem

    # Comando /xp
    @app_commands.guilds(guild)
    @app_commands.command(name="xp", description="Veja seu XP atual.")
    async def xp(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        xp = get_xp(user.id)
        await interaction.response.send_message(f"{user.mention} tem {xp} XP!", ephemeral=True)

    # Comando /rank
    @app_commands.guilds(guild)
    @app_commands.command(name="rank", description="Veja o ranking de XP do servidor.")
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

    @app_commands.guilds(guild)
    @app_commands.command(name="ping", description="Ping da Zero Two.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong!🏓\n **Latência**: {round(self.bot.latency * 1000)}ms", ephemeral=True)
        logging.info(f"Ping: {interaction.user} verificou o ping.")

    @app_commands.guilds(guild)
    @app_commands.command(name="admin", description="Menu de administração")
    async def admin(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
            logging.warning(f"{interaction.user} tentou acessar admin sem permissão.")
            return
        await interaction.response.send_message("🛠️ Selecione uma função administrativa:", view=AdminMenu(), ephemeral=True)
        logging.info(f"Admin menu acessado por {interaction.user}")

    @app_commands.command(name="oi", description="Receba um cumprimento personalizado.")
    async def oi(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Olá, {interaction.user.mention}! Eu sou a Zero Two! 💖", ephemeral=True)
        logging.info(f"Oi: {interaction.user} recebeu um oi.")

    @app_commands.command(name="info", description="Mostra informações sobre a Zero Two.")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Zero Two 💖",
            description="Serei sua nova assistente, bastante estilosa!",
            color=discord.Color.pink()
        )
        embed.add_field(name="Criador", value="Você mesmo!")
        embed.set_footer(text="Feito com discord.py")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logging.info(f"Info: {interaction.user} visualizou as informações.")

    @app_commands.command(name="soma", description="Soma dois números inteiros.")
    async def soma(self, interaction: discord.Interaction, num1: int, num2: int):
        resultado = num1 + num2
        await interaction.response.send_message(f"A soma de {num1} + {num2} é: {resultado}", ephemeral=True)
        logging.info(f"Soma: {interaction.user} somou {num1} + {num2} = {resultado}")

    @app_commands.command(name="calc", description="Calcula uma expressão matemática avançada.")
    async def calc(self, interaction: discord.Interaction, *, expressao: str):
        expressao = re.sub(r'[^0-9\+\-\*\/\(\)\.\,\%\!\ ]', '', expressao.lower()).replace(',', '.')
        expressao = parse_fatorial(expressao)
        try:
            resultado = eval_expr(expressao)
            await interaction.response.send_message(f"O resultado de `{expressao}` é: {resultado}", ephemeral=True)
            logging.info(f"Calc: {interaction.user} calculou {expressao} = {resultado}")
        except Exception as e:
            await interaction.response.send_message(f"❌ Não consegui calcular: {e}\nExemplo válido: `3! + 2**3 - 4//2`", ephemeral=True)
            logging.error(f"Erro ao calcular {expressao}: {e}")

    @app_commands.command(name="ferramentas", description="Acesse ferramentas úteis.")
    async def ferramentas(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔧 Selecione uma ferramenta:", view=FerramentasMenu(), ephemeral=True)
        logging.info(f"Ferramentas: {interaction.user} abriu o menu de ferramentas.")

async def setup(bot):
    await bot.add_cog(Gerais(bot))