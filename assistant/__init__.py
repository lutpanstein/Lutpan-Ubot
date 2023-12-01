# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from Lutpan import *
from Lutpan import _lutpan_cache
from Lutpan._misc import owner_and_sudos
from Lutpan._misc._assistant import asst_cmd, callback, in_pattern
from Lutpan.fns.helper import *
from Lutpan.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = lutpan_bot.full_name
OWNER_ID = lutpan_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException:
        return await event.edit("`Ada yang salah`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
