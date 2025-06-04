import discord
from discord.ext import commands
from discord import app_commands
import re
import ast
import operator

class Gerais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="oi", description="Receba um cumprimento personalizado.")
    async def oi(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Olá, {interaction.user.mention}! Eu sou a Zero Two! 💖"
        )

    @app_commands.command(name="info", description="Mostra informações sobre a Zero Two.")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Zero Two 💖",
            description="Serei sua nova assistente, bastante estilosa!",
            color=discord.Color.magenta()
        )
        embed.add_field(name="Criador", value="Você mesmo!")
        embed.set_footer(text="Feito com discord.py")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ajuda", description="Mostra a lista de comandos da Zero Two.")
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💖 Comandos da Zero Two 💖",
            description="Clique nos botões abaixo para saber mais sobre cada comando!",
            color=discord.Color.purple()
        )

        embed.set_thumbnail(url="https://i.pinimg.com/736x/5e/30/15/5e30153b76d17935e1a8729b1cf89b1a.jpg")

        view = discord.ui.View()

        buttons = {
            "oi": "Receba um cumprimento personalizado.",
            "soma": "Soma dois números. Exemplo: /soma num1:2 num2:2",
            "info": "Informações sobre a Zero Two.",
            "calc": "Calcula uma expressão matemática simples. Exemplo: /calc expressão:2+2"
        }

        for label, desc in buttons.items():
            button = discord.ui.Button(label=label, style=discord.ButtonStyle.primary)

            async def callback(interaction, desc=desc):
                await interaction.response.send_message(desc, ephemeral=True)

            button.callback = callback
            view.add_item(button)

        embed.set_footer(
            text="Estou aqui para te ajudar ❤️",
            icon_url="https://i.pinimg.com/736x/bb/54/e7/bb54e7b04744cc35a15860b62b66ba8e.jpg"
        )

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="soma", description="Soma dois números inteiros.")
    async def soma(self, interaction: discord.Interaction, num1: int, num2: int):
        resultado = num1 + num2
        await interaction.response.send_message(
            f"A soma de {num1} + {num2} é: {resultado}"
        )

    @app_commands.command(name="calc", description="Calcula uma expressão matemática simples.")
    async def calc(self, interaction: discord.Interaction, *, expressao: str):
        expressao = expressao.lower()
        expressao = re.sub(r'[^0-9\+\-\*\/\(\)\.\,]', '', expressao)
        expressao = expressao.replace(',', '.')

        try:
            resultado = self.eval_expr(expressao)
            await interaction.response.send_message(f"O resultado de `{expressao}` é: {resultado}")
        except Exception as e:
            await interaction.response.send_message(
                f"Desculpe, não consegui entender ou calcular isso. Erro: {e}"
            )

    def eval_expr(self, expr):
        operadores = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        def eval_(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return operadores[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):
                return operadores[type(node.op)](eval_(node.operand))
            else:
                raise TypeError(node)

        node = ast.parse(expr, mode='eval').body
        return eval_(node)

async def setup(bot):
    await bot.add_cog(Gerais(bot))
