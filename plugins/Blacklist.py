# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

"""
◈ Perintah Tersedia

• `{i} blacklist <kata>`
    Daftar hitam kan kata yang dipilih.

• `{i} remblacklist <kata>`
     Hapus kata dari daftar hitam.
     
• `{i} listblacklist`
     Lihat Semua Daftar Kata Terlarang .
"""


from . import get_help

__doc__ = get_help("help_blacklist")


from Lutpan.dB.blacklist_db import (
    add_blacklist,
    get_blacklist,
    list_blacklist,
    rem_blacklist,
)
from . import events, get_string, udB, lutpan_bot, lutpan_cmd

     
@lutpan_cmd(pattern="blacklist( (.*)|$)", admins_only=True)
async def af(e):
    wrd = e.pattern_match.group(1).strip()
    chat = e.chat_id
    if not (wrd):
        return await e.eor(get_string("blk_1"), time=5)
    wrd = e.text[11:]
    heh = wrd.split(" ")
    for z in heh:
        add_blacklist(int(chat), z.lower())
    lutpan_bot.add_handler(blacklist, events.NewMessage(incoming=True))
    await e.eor(get_string("blk_2").format(wrd))


@lutpan_cmd(pattern="remblacklist( (.*)|$)", admins_only=True)
async def rf(e):
    wrd = e.pattern_match.group(1).strip()
    chat = e.chat_id
    if not wrd:
        return await e.eor(get_string("blk_3"), time=5)
    wrd = e.text[14:]
    heh = wrd.split(" ")
    for z in heh:
        rem_blacklist(int(chat), z.lower())
    await e.eor(get_string("blk_4").format(wrd))


@lutpan_cmd(pattern="listblacklist$", admins_only=True)
async def lsnote(e):
    if x := list_blacklist(e.chat_id):
        sd = get_string("blk_5")
        return await e.eor(sd + x)
    await e.eor(get_string("blk_6"))


async def blacklist(e):
    if x := get_blacklist(e.chat_id):
        text = e.text.lower().split()
        if any((z in text) for z in x):
            try:
                await e.delete()
            except BaseException:
                pass


if udB.get_key("BLACKLIST_DB"):
    lutpan_bot.add_handler(blacklist, events.NewMessage(incoming=True))
