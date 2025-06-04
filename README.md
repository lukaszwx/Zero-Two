# Zero Two Bot Discord 🤖💖

Zero Two é uma bot de Discord escrito em Python com **discord.py** que oferece ferramentas úteis, comandos administrativos e interativos para seu servidor. Ela será responsavel por administrar seu servidor ou ser sua assistência. Por enquanto, zero two está em fase de criação onde estão sendo implementadas novas funções.

---

## Funcionalidades

- Comandos slash fáceis de usar: cumprimentos, informações, somas e cálculo de expressões.
- Menu administrativo com opções para silenciar, expulsar e banir membros, fazer anúncios e limpar mensagens.
- Ferramentas interativas:
  - Calculadora integrada via modal.
  - Relógio com horário atual.
  - Frases motivacionais para os membros.
- Utiliza views persistentes para menus interativos e melhor experiência de usuário.
- Sincronização rápida de comandos específicos para o seu servidor (guild).

## Funcionalidades futuras ⏳⌚
 - Implementação de API
 - Funcionalidades de Administador
 - Suporte para vendas(se for usar em servidor de loja discord)
 - implementação de sistema de vendas
 - implementação de API (Mercado Pago)
 - implementação de IA( ex: chat gpt)


---

## Comandos principais
- /oi – Receba um cumprimento personalizado do bot.
- /info – Veja informações sobre o bot Zero Two.
- /soma num1 num2 – Soma dois números inteiros.
- /calc expressao – Calcula uma expressão matemática simples.
- /admin – Abre o menu administrativo (apenas administradores).
- /ferramentas – Abre o menu de ferramentas úteis.
- /ping – Responde com "Pong!" e a latência do bot.


## Tecnologias

- Python 3.8+
- [discord.py](https://discordpy.readthedocs.io/en/stable/) - Biblioteca para bots Discord
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Para carregar variáveis de ambiente

---

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/seurepositorio.git
   cd seurepositorio


#### Código antigo ####
<!--import discord
from discord.ext import commands
from discord import app_commands, ui
import re
import ast
import operator
from datetime import datetime
import random
import math

# ID do servidor (guild) onde os comandos serão registrados.
GUILD_ID = 1378054602955554836
guild = discord.Object(id=GUILD_ID)

# ------------------- CLASSES ADMIN ------------------- #

class AdminSelec(ui.Select):
    """
    Classe que representa um menu de seleção para funções administrativas.
    
    Permite que o usuário escolha entre várias ações administrativas, como silenciar,
    desmutar, banir, expulsar membros, fazer anúncios e limpar mensagens.
    """
    def __init__(self):
        options = [
            discord.SelectOption(label="Silenciar membro", description="Coloca um membro em timeout"),
            discord.SelectOption(label="Desmutar membro", description="Remove timeout de um membro"),
            discord.SelectOption(label="Banir membro", description="Bane um membro do server"),
            discord.SelectOption(label="Expulsar membro", description="Expulsa um membro do server"),
            discord.SelectOption(label="Anunciar", description="Faz um anúncio no canal"),
            discord.SelectOption(label="Limpar mensagens", description="Apaga as mensagens do canal"),
        ]
        super().__init__(placeholder="Escolha uma função...", options=options, custom_id="admin_select")

    async def callback(self, interaction: discord.Interaction):
        """
        Callback chamado quando uma opção é selecionada.
        
        Envia uma resposta ao usuário com base na escolha feita.
        """
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

class AdminMenu(ui.View):
    """
    Classe que representa a visualização do menu de administração.
    
    Contém um item de seleção para escolher funções administrativas.
    """
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AdminSelec())

# ------------------- CALCULADORA ------------------- #

class CalculadoraModal(ui.Modal, title="Calculadora da Zero Two"):
    """
    Modal para entrada de expressões matemáticas.
    
    Permite que o usuário insira uma expressão e calcula o resultado.
    """
    expressao = ui.TextInput(
        label="Digite a expressão",
        style=discord.TextStyle.short,
        placeholder="Exemplo: 2+3*5",
        max_length=50
    )

    def __init__(self, select):
        super().__init__()
        self.select = select

    async def on_submit(self, interaction: discord.Interaction):
        """
        Callback chamado quando o modal é enviado.
        
        Avalia a expressão matemática e envia o resultado ao usuário.
        """
        expr = self.expressao.value.lower()
        expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\,]', '', expr)
        expr = expr.replace(',', '.')
        try:
            resultado = self.select.eval_expr(expr)
            await interaction.response.send_message(f"Resultado de `{expr}`: **{resultado}**", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Expressão inválida. Erro: {e}", ephemeral=True)

# ------------------- FERRAMENTAS ------------------- #

class FerramentasSelect(ui.Select):
    """
    Classe que representa um menu de seleção para ferramentas úteis.
    
    Permite que o usuário escolha entre uma calculadora, relógio e frases motivacionais.
    """
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

    def eval_expr(self, expr):
        """
        Avalia uma expressão matemática usando a árvore de sintaxe abstrata (AST).
        
        Permite operações básicas como adição, subtração, multiplicação e divisão.
        """
        operadores = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        def eval_(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp):
                return operadores[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):
                return operadores[type(node.op)](eval_(node.operand))
            else:
                raise TypeError(f"Operação inválida: {node}")

        node = ast.parse(expr, mode='eval').body
        return eval_(node)

    async def callback(self, interaction: discord.Interaction):
        """
        Callback chamado quando uma opção é selecionada.
        
        Executa a ação correspondente à escolha do usuário, como abrir a calculadora,
        mostrar o horário atual ou enviar uma frase motivacional.
        """
        escolha = self.values[0]
        if escolha == 'Calculadora':
            modal = CalculadoraModal(self)
            await interaction.response.send_modal(modal)
        elif escolha == 'Relógio':
            agora = datetime.now().strftime("%H:%M:%S")
            await interaction.response.send_message(f'🕒 Agora são {agora}.', ephemeral=True)
        elif escolha == 'Motivação':
            frase = random.choice(self.frases_motivacao)
            await interaction.response.send_message(frase, ephemeral=True)

class FerramentasMenu(ui.View):
    """
    Classe que representa a visualização do menu de ferramentas úteis.
    
    Contém um item de seleção para escolher entre as ferramentas disponíveis.
    """
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FerramentasSelect())

# ------------------- COG PRINCIPAL ------------------- #

class Gerais(commands.Cog):
    """
    Classe principal que contém os comandos do bot.
    
    Inclui comandos para administração, cumprimentos, informações e ferramentas.
    """
    def __init__(self, bot):
        self.bot = bot
    @app_commands.guilds(guild)
    @app_commands.command(name="ping", description="Ping da Zero Two.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong!🏓\n **Latência**: {round(self.bot.latency *1000)}ms")
        
    @app_commands.command(name="admin", description="Menu de administração")
    @app_commands.guilds(guild)
    async def admin(self, interaction: discord.Interaction):
        """
        Comando que exibe o menu de administração.
        
        Verifica se o usuário tem permissões de administrador antes de mostrar o menu.
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
            return
        view = AdminMenu()
        await interaction.response.send_message("🛠️ Selecione uma função administrativa:", view=view, ephemeral=True)

    @app_commands.command(name="oi", description="Receba um cumprimento personalizado.")
    async def oi(self, interaction: discord.Interaction):
        """
        Comando que envia um cumprimento personalizado ao usuário.
        """
        await interaction.response.send_message(f"Olá, {interaction.user.mention}! Eu sou a Zero Two! 💖")

    @app_commands.command(name="info", description="Mostra informações sobre a Zero Two.")
    async def info(self, interaction: discord.Interaction):
        """
        Comando que envia informações sobre o bot Zero Two em um embed.
        """
        embed = discord.Embed(
            title="Zero Two 💖",
            description="Serei sua nova assistente, bastante estilosa!",
            color=discord.Color.pink()
        )
        embed.add_field(name="Criador", value="Você mesmo!")
        embed.set_footer(text="Feito com discord.py")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="soma", description="Soma dois números inteiros.")
    async def soma(self, interaction: discord.Interaction, num1: int, num2: int):
        """
        Comando que soma dois números inteiros e envia o resultado.
        """
        resultado = num1 + num2
        await interaction.response.send_message(f"A soma de {num1} + {num2} é: {resultado}")

    @app_commands.command(name="calc", description="Calcula uma expressão matemática simples.")
    async def calc(self, interaction: discord.Interaction, *, expressao: str):
        """
        Comando que calcula uma expressão matemática simples fornecida pelo usuário.
        
        Limpa a expressão de caracteres inválidos e tenta calcular o resultado.
        """
        expressao = expressao.lower()
        expressao = re.sub(r'[^0-9\+\-\*\/\(\)\.\,]', '', expressao)
        expressao = expressao.replace(',', '.')
        try:
            resultado = self.eval_expr(expressao)
            await interaction.response.send_message(f"O resultado de `{expressao}` é: {resultado}")
        except Exception as e:
            await interaction.response.send_message(f"Desculpe, não consegui entender ou calcular isso. Erro: {e}")

    def eval_expr(self, expr):
        """
        Avalia uma expressão matemática usando a árvore de sintaxe abstrata (AST).
        
        Permite operações básicas como adição, subtração, multiplicação e divisão.
        """
        operadores = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

        def eval_(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp):
                return operadores[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):
                return operadores[type(node.op)](eval_(node.operand))
            else:
                raise TypeError(f"Operação inválida: {node}")

        node = ast.parse(expr, mode='eval').body
        return eval_(node)

    @app_commands.command(name="ferramentas", description="Acesse ferramentas úteis.")
    async def ferramentas(self, interaction: discord.Interaction):
        """
        Comando que exibe o menu de ferramentas úteis.
        """
        view = FerramentasMenu()
        await interaction.response.send_message("🔧 Selecione uma ferramenta:", view=view, ephemeral=True)

# ------------------- SETUP ------------------- #

async def setup(bot):
    """
    Função de configuração que adiciona a cog 'Gerais' ao bot.
    """
    await bot.add_cog(Gerais(bot))
>