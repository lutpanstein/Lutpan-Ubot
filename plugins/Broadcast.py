# ayra - userbot
# copyright (c) 2021-2022 senpai80
#
# this file is a part of < https://github.com/senpai80/ayra/ >
# please read the gnu affero general public license in
# <https://www.github.com/senpai80/ayra/blob/main/license/>.
"""
✘ **bantuan untuk broadcast**

๏ **perintah:** `gcast`
◉ **keterangan:** kirim pesan ke semua obrolan grup.

๏ **perintah:** `gucast`
◉ **keterangan:** kirim pesan ke semua pengguna pribadi.

๏ **perintah:** `addbl`
◉ **keterangan:** tambahkan grup ke dalam anti gcast.

๏ **perintah:** `delbl`
◉ **keterangan:** hapus grup dari daftar anti gcast.

๏ **perintah:** `blchat`
◉ **keterangan:** melihat daftar anti gcast.
"""
import asyncio

from Lutpan.dB import DEVLIST
from Lutpan.fns.tools import create_tl_btn, format_btn, get_msg_button
from telethon.errors.rpcerrorlist import FloodWaitError

from . import *
from ._inline import something


@lutpan_cmd(pattern="[Gg][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gcast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eor(
            event, "`ketik pesan bejirrr minimal direply biar bisa gikess`"
        )
    kk = await event.eor("`lagi ngirim ya bejirrr meskipun gikesan kalian ga sederes gikesan lutpan`")
    er = 0
    done = 0
    err = ""
    chat_blacklist = udb.get_key("GBLACKLISTS") or []
    chat_blacklist.append(-1001287188817)
    udb.set_key("GBLACKLISTS", chat_blacklist)
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            
            if chat not in chat_blacklist and chat not in NOSPAM_CHAT:
                try:
                    await event.client.send_message(chat, msg)
                    done += 1
                except floodwaiterror as fw:
                    await asyncio.sleep(fw.seconds + 10)
                    try:
                        await event.client.send_message(
                                chat, msg)
                        done += 1
                    except exception as rr:
                        err += f"• {rr}\n"
                        er += 1
                except baseexception as h:
                    err += f"• {str(h)}" + "\n"
                    er += 1
    await kk.edit(f"**KEKIRIM KE {done} GECEH YA AJG, YG {er} gamasuk.Kata Lutpan lu dimute kali wkwkwkwk.**")


@lutpan_cmd(pattern="[gG][u][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gucast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eor(
            event, "`bejirrr apanya yg mau dikirim`"
        )
    kk = await event.eor("`lagi dikirim meskipun ga sederes gikesan lutpan`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in DEVLIST:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except floodwaiterror as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except baseexception:
                    er += 1
    await kk.edit(f"udah kekirim di {done} obrolan bang, yg {er} gamasuk wkwkwkwk")


@lutpan_cmd(pattern="addbl")
async def blacklist_(event):
    await gblacker(event, "add")


@lutpan_cmd(pattern="delbl")
async def ungblacker(event):
    await gblacker(event, "remove")


@lutpan_cmd(pattern="blchat")
async def chatbl(event):
    id = event.chat_id
    if xx := list_bl(id):
        sd = "**❏ daftar blacklist gcast**\n\n"
        return await event.eor(sd + xx)
    await event.eor("**belum ada daftar**")


async def gblacker(event, type_):
    args = event.text.split()
    if len(args) > 2:
        return await event.eor("**gunakan format:**\n `delbl` or `addbl`")
    chat_id = none
    chat_id = int(args[1]) if len(args) == 2 else event.chat_id
    if type_ == "add":
        add_gblacklist(chat_id)
        await event.eor(f"**KATA LUTPAN TANDAIN AJA INI GC PELIT KLO NYURUH ADDBL... UDAH DONE YA AJG**\n`{chat_id}`")
    elif type_ == "remove":
        rem_gblacklist(chat_id)
        await event.eor(f"**NAH CAKEP KATA LUTPAN KLO DIUNBL.. SEMANGAT APUSIN GIKESNYA UDAH GA KE BL**\n`{chat_id}`")
