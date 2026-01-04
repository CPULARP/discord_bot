import logging

import discord

from Shared.Utilities.discord_utilities import CPU_GUILD_ID, check_admin_role, check_npc_role, send_message_safe
from Shared.bot_instance import cpu_discord_bot

CPU_GUILD = discord.Object(id=CPU_GUILD_ID)


@cpu_discord_bot.tree.command(name="help", description="List all available slash commands and their descriptions.",
                              guild=CPU_GUILD)
async def help_command(interaction: discord.Interaction):
    help_message = await _get_help_text(interaction)
    await send_message_safe(interaction, f"Available commands:\n{help_message}", ephemeral=True)


async def _get_help_text(interaction: discord.Interaction):
    commands_list = [
        ("scavenge", "Search for items in various locations."),
        ("pickpocket", "Attempt to steal from someone."),
        ("loot", "Roll for loot from a loot table."),
        ("hack", "Attempt to brute-force a security code."),
        ("guess", "Make a guess in Mastermind."),
        ("item", "Search for an item in the spreadsheet."),
        ("rule", "Returns the definition of a CPU Call, Function, or keyword."),
        ("escape", "Roll for an escape attempt.")
    ]

    if await check_npc_role(interaction, send_response=False):
        commands_list.extend([
            ("combat_npc", "Generate an NPC for combat."),
            ("roleplaynpc", "Generate an NPC for roleplay."),
            ("write", "Post an item to the card writing channel.")
        ])

    if await check_admin_role(interaction, send_response=False):
        commands_list.extend([
            ("combat_npc", "Generate an NPC for combat."),
            ("roleplaynpc", "Generate an NPC for roleplay."),
            ("set_code", "Set a secret code for Mastermind."),
            ("startindynews", "Start Indy news updates."),
            ("startseattlenews", "Start Seattle news updates."),
            ("stopindynews", "Stop Indy news updates."),
            ("stopseattlenews", "Stop Seattle news updates."),
            ("write", "Post an item to the card writing channel.")
        ])

    logging.info(commands_list)
    help_message = "\n".join([f"/{cmd} - {desc}" for cmd, desc in commands_list])
    return help_message
