import discord
from discord.ext import commands


class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, prefix: str) -> None:
        if len(prefix) > 10:
            await ctx.send("Prefix must be less than 10 characters long")
            return
        else:
            self.bot.prefixes[ctx.guild.id] = prefix
            async with self.bot.pool.acquire() as conn:

                await conn.execute("INSERT INTO guilds (id, prefix) "
                                   "VALUES ($1, $2) ON CONFLICT (id) DO "
                                   "UPDATE SET prefix = $3 WHERE guilds.id = $4",
                                   ctx.guild.id,
                                   prefix,
                                   prefix,
                                   ctx.guild.id)

                e = discord.Embed(title='Success!',
                                  description=f"The prefix for this server has been set to `{prefix}`",
                                  colour=discord.Colour.green())
                await ctx.send(embed=e)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def bdchannel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Sets the birthday alert channel for a particular guild"""

        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE guilds SET bdayalert = $1 WHERE id = $2", channel.id, ctx.guild.id)
            e = discord.Embed(title='Success!',
                              description=f'The channel {channel.mention} will be used for auto birthday alerts',
                              colour=discord.Colour.green())
            await ctx.send(embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(ConfigCommands(bot))
