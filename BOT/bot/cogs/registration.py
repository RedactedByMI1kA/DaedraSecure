import re

import nextcord
from bot.cogs.utils.database_models import RegistrationRecord
from nextcord.ext import commands

from .utils.base_cog import BaseCog


class Registration(BaseCog):
    registration_message_regex = re.compile("1\.[\s]?(.+)\n2\.[\s]?(.+)")

    @property
    def registration_channel(self) -> nextcord.TextChannel:
        return self.bot.get_channel(
            self.bot.config.registration.registration_channel_id
        )

    @property
    def bot_send_channel(self) -> nextcord.TextChannel:
        return self.bot.get_channel(self.bot.config.registration.bot_send_channel_id)

    @property
    def registration_role(self) -> nextcord.Role:
        return self.registration_channel.guild.get_role(
            self.bot.config.registration.registration_role_id
        )

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return

        await self.bot.wait_until_ready()

        if message.channel != self.registration_channel:
            return

        await message.delete()

        result = self.registration_message_regex.match(
            nextcord.utils.escape_markdown(message.content)
        )

        if result is None:
            return

        user_id, call_name = result.groups()
        record = await RegistrationRecord.create(
            guild_id=message.guild.id, member_id=message.author.id
        )

        embed = nextcord.Embed(
            title=self.bot.default_phrases.registration.title_fmt,
            description=self.bot.default_phrases.registration.description_fmt.format(
                member=message.author
            ),
            colour=nextcord.Colour.dark_theme(),
        )

        embed.set_thumbnail(url=message.author.display_avatar.url)

        embed.add_field(
            name=self.bot.default_phrases.registration.user_id_name,
            value=user_id,
            inline=False,
        )

        embed.add_field(
            name=self.bot.default_phrases.registration.call_name,
            value=call_name,
            inline=False,
        )

        embed.add_field(
            name=self.bot.default_phrases.registration.number,
            value=str(record.id).rjust(4, "0"),
            inline=False,
        )

        await message.author.add_roles(self.registration_role)
        await self.bot_send_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Registration(bot))
