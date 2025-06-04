from discord.ext import commands

class Ping(commands.Cog):
    """
    Classe que contém o comando de ping para o bot.
    
    Este comando responde com 'Pong!' quando chamado.
    """

    def __init__(self, bot):
        """
        Inicializa a classe Ping com a instância do bot.
        
        :param bot: Instância do bot Discord.
        """
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Comando que responde com '🏓 Pong!'.
        
        :param ctx: Contexto da mensagem onde o comando foi chamado.
        """
        await ctx.send('🏓 Pong!')

async def setup(bot):
    """
    Função de configuração que adiciona a cog 'Ping' ao bot.
    
    :param bot: Instância do bot Discord.
    """
    await bot.add_cog(Ping(bot))

