import json
import logging
import os

import discord
from discord import Interaction, app_commands

from Shared.Utilities.discord_utilities import (CHAPTER_INDY, CHAPTER_SEATTLE, CPU_GUILD_ID, INDY_ITEM_CARD_CHANNEL_ID,
                                                INDY_JOB_QUEUE_CATEGORY_ID, INDY_JOB_QUEUE_CHANNEL_ID,
                                                INDY_LOGISTICS_CATEGORY_ID,
                                                INDY_STAFF_AFTER_SIM_CATEGORY_ID, INDY_STAFF_TO_DO_CATEGORY_ID,
                                                SEATTLE_ITEM_CARD_CHANNEL_ID,
                                                SEATTLE_JOB_QUEUE_CATEGORY_ID, SEATTLE_JOB_QUEUE_CHANNEL_ID,
                                                SEATTLE_LOGISTICS_CATEGORY_ID,
                                                SEATTLE_STAFF_AFTER_SIM_CATEGORY_ID,
                                                SEATTLE_STAFF_TO_DO_CATEGORY_ID, USER_CITY_FILE,
                                                send_message_safe,
                                                user_has_only_indy_role,
                                                user_has_only_seattle_role)
from Shared.bot_instance import cpu_discord_bot

CPU_GUILD = discord.Object(id=CPU_GUILD_ID)

if not os.path.exists(USER_CITY_FILE):
    with open(USER_CITY_FILE, "w") as f:
        json.dump({}, f)


async def get_city_for_user(interaction: Interaction) -> str:
    user_id = str(interaction.user.id)

    try:
        with open(USER_CITY_FILE, "r") as f:
            overrides = json.load(f)
    except Exception as e:
        logging.warning(f"Failed to read overrides file: {e}")
        overrides = {}

    city_override = overrides.get(user_id)
    if city_override:
        city_override_lower = city_override.lower()
        if city_override_lower == "indy":
            return CHAPTER_INDY
        elif city_override_lower == "seattle":
            return CHAPTER_SEATTLE
        else:
            logging.warning(f"User {user_id} has invalid city override: {city_override}")

    if await user_has_only_indy_role(interaction):
        return CHAPTER_INDY
    if await user_has_only_seattle_role(interaction):
        return CHAPTER_SEATTLE

    logging.warning(f"User {user_id} has no city context, defaulting to Seattle")
    return CHAPTER_SEATTLE


async def get_logistics_category_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_LOGISTICS_CATEGORY_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_LOGISTICS_CATEGORY_ID
    else:
        category_id = SEATTLE_LOGISTICS_CATEGORY_ID
    category = interaction.guild.get_channel(category_id)
    return category


async def get_later_category_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_STAFF_AFTER_SIM_CATEGORY_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_STAFF_AFTER_SIM_CATEGORY_ID
    else:
        category_id = SEATTLE_STAFF_AFTER_SIM_CATEGORY_ID
    category = interaction.guild.get_channel(category_id)
    return category


async def get_staff_to_do_category_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_STAFF_TO_DO_CATEGORY_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_STAFF_TO_DO_CATEGORY_ID
    else:
        category_id = SEATTLE_STAFF_TO_DO_CATEGORY_ID
    category = interaction.guild.get_channel(category_id)
    return category


async def get_job_queue_category_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_JOB_QUEUE_CATEGORY_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_JOB_QUEUE_CATEGORY_ID
    else:
        category_id = SEATTLE_JOB_QUEUE_CATEGORY_ID
    category = interaction.guild.get_channel(category_id)
    return category


async def get_job_queue_channel_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_JOB_QUEUE_CHANNEL_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_JOB_QUEUE_CHANNEL_ID
    else:
        category_id = SEATTLE_JOB_QUEUE_CHANNEL_ID
    category = interaction.guild.get_channel(category_id)
    return category


async def get_card_writing_channel_category_for_user(interaction: discord.Interaction):
    city = await get_city_for_user(interaction)
    if city == CHAPTER_INDY:
        category_id = INDY_ITEM_CARD_CHANNEL_ID
    elif city == CHAPTER_SEATTLE:
        category_id = SEATTLE_ITEM_CARD_CHANNEL_ID
    else:
        category_id = SEATTLE_ITEM_CARD_CHANNEL_ID
    category = interaction.guild.get_channel(category_id)
    return category


@cpu_discord_bot.tree.command(name="overridecity", description="Set your city context (indy or seattle)",
                              guild=CPU_GUILD)
@app_commands.describe(city="Optional override: indy or seattle")
async def override_command(interaction: Interaction, city: str):
    await _override(interaction, city)


async def _override(interaction: Interaction, city: str):
    city_lower = city.lower()
    if city_lower not in {"indy", "seattle"}:
        await send_message_safe(interaction, f"Invalid city '{city}'. Please use 'indy' or 'seattle'.", ephemeral=True)
        return

    overrides = {}
    if os.path.exists(USER_CITY_FILE):
        with open(USER_CITY_FILE, "r") as f:
            try:
                overrides = json.load(f)
            except json.JSONDecodeError:
                overrides = {}

    overrides[str(interaction.user.id)] = city_lower

    with open(USER_CITY_FILE, "w") as f:
        json.dump(overrides, f, indent=2)

    await send_message_safe(interaction, f"Your city override has been set to '{city_lower}'.", ephemeral=True)
