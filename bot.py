#primeira bot zero two( ainda em fase de desenvolvimento)


import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configura os intents do bot para receber eventos necessários.
intents = discord.Intents.default()
intents.message_content = True  # Permite acesso ao conteúdo das mensagens.

# ID do servidor (guild) onde os comandos slash serão sincronizados.
MY_GUILD_ID = 1378054602955554836
MY_GUILD = discord.Object(id=MY_GUILD_ID)

class MyBot(commands.Bot):
    """
    Classe personalizada do bot Discord que herda de commands.Bot.
    
    Gerencia o carregamento de extensões (cogs), views persistentes
    e sincronização dos comandos slash para uma guild específica.
    """
    def __init__(self):
        # Inicializa o bot com prefixo de comando e intents configurados.
        super().__init__(command_prefix='02!', intents=intents)
        self.persistent_views_added = False  # Flag para garantir adição única das views.

    async def setup_hook(self):
        """
        Método executado quando o bot está sendo configurado antes de entrar online.
        
        - Carrega os cogs necessários.
        - Adiciona as views persistentes para manter menus ativos.
        - Sincroniza os comandos slash apenas para a guild especificada.
        """
        # Carrega o cog 'gerais' que contém comandos e views.
        await self.load_extension('cogs.gerais')

        await self.load_extension('cogs.xp')

        # Adiciona views persistentes se ainda não adicionadas para manter menus vivos após reinício.
        if not self.persistent_views_added:
            from cogs.gerais import FerramentasMenu, AdminMenu
            self.add_view(FerramentasMenu())
            self.add_view(AdminMenu())
            self.persistent_views_added = True

        # Sincroniza comandos do bot para o servidor específico definido por MY_GUILD.
        await self.tree.sync(guild=MY_GUILD)
        print("✅ Slash commands sincronizados com o servidor.")

# Instância do bot personalizado.
bot = MyBot()

@bot.event
async def on_ready():
    """
    Evento disparado quando o bot finaliza a conexão e está pronto para uso.
    
    Imprime no console informações do bot e do servidor conectado,
    além de listar os comandos registrados para conferência.
    """
    print(f'✅ Bot {bot.user} está online e pronto!')
    guild = bot.get_guild(MY_GUILD_ID)
    if guild:
        print(f"Conectado ao servidor: {guild.name} (ID: {guild.id})")
    else:
        print("⚠️ Guild não encontrada!")

    # Debug: lista os comandos slash registrados nessa guild.
    cmds = await bot.tree.fetch_commands(guild=MY_GUILD)
    print("Comandos registrados neste servidor:")
    for cmd in cmds:
        print(f"- {cmd.name}: {cmd.description}")

async def main():
    """
    Função principal para iniciar o bot com gerenciamento assíncrono.
    
    Usa o gerenciador de contexto async para garantir um start e shutdown corretos.
    """
    async with bot:
        await bot.start(TOKEN)

if __name__ == '__main__':
    # Inicia o loop assíncrono principal do bot.
    asyncio.run(main())

