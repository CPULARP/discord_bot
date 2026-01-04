# Make sure that all the Logistics category tickets have the appropriate access set up
import logging

import discord
from discord.ext import tasks

from Shared.Utilities.discord_utilities import CPU_GUILD_ID, INDY_LOGISTICS_CATEGORY_ID, LOGISTICS_ROLE_ID, \
    SEATTLE_LOGISTICS_CATEGORY_ID
from Shared.bot_instance import cpu_discord_bot


@tasks.loop(minutes=5)
async def enforce_role_access():
    logging.debug(f"enforce_role_access: tick")
    guild = cpu_discord_bot.get_guild(CPU_GUILD_ID)

    indy_logistics_category = guild.get_channel(INDY_LOGISTICS_CATEGORY_ID)
    if not indy_logistics_category or not isinstance(indy_logistics_category, discord.CategoryChannel):
        logging.error(f"Could not find {indy_logistics_category.name}.")
    await _enforce_role_access(indy_logistics_category)

    seattle_logistics_category = guild.get_channel(SEATTLE_LOGISTICS_CATEGORY_ID)
    if not seattle_logistics_category or not isinstance(seattle_logistics_category, discord.CategoryChannel):
        logging.error(f"Could not find {seattle_logistics_category.name}.")
    await _enforce_role_access(seattle_logistics_category)


async def _enforce_role_access(category):
    guild = cpu_discord_bot.get_guild(CPU_GUILD_ID)
    role = guild.get_role(LOGISTICS_ROLE_ID)
    if not role:
        logging.error(f"_enforce_role_access: Could not find logistics role.")
        return

    for channel in category.channels:
        perms = channel.overwrites_for(role)

        if perms.read_messages is not True or perms.send_messages is not True:
            try:
                await channel.set_permissions(role, read_messages=True, send_messages=True)
                logging.info(f"_enforce_role_access: Fixed access for {role.name} in {channel.name}")
            except Exception as e:
                logging.error(f"_enforce_role_access: Failed to update {channel.name}: {e}")


@enforce_role_access.before_loop
async def before_enforce_role_access():
    await cpu_discord_bot.wait_until_ready()
    logging.info("before_enforce_role_access: Starting logistics role access enforcement...")
