# @riizzvbss
"""
◈ Perintah Tersedia

• `{i}ass`
   Salam Lengkap

• `{i}as`
   Assalamu'alaikum

• `{i}ws`
   Jawab Salam
   
• `{i}ks`
   Kenalan Salam
   
• `{i}jws`
   Istighfar Salam
   
• `{i}3x`
    Bisa Kali

• `{i}kg`
    Keren lu gitu
"""

from time import sleep
from . import (
    eor,
    lutpan_cmd,
)

@lutpan_cmd(pattern="ass$")
async def _(event):
    await event.eor("**Assalamu'alaikum Warohmatulohi Wabarokatu**")


@lutpan_cmd(pattern="as$")
async def _(event):
    await event.eor("**Assalamu'alaikum**")
    
@lutpan_cmd(pattern="ws$")
async def _(event):
    await event.eor("**Wa'alaikumussalam**")

    
@lutpan_cmd(pattern="ks$")
async def _(event):
    xx = await event.eor("**Hy kaa 🥺**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@lutpan_cmd(pattern="jws$")
async def _(event):
    xx = await event.eor(event, "**Astaghfirullah, Jawab salam dong**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum**")


@lutpan_cmd(pattern="3x$")
async def _(event):
    xx = await event.eor("**Bismillah, 3x**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum Bisa Kali**")
    
@lutpan_cmd(pattern="kg$")
async def _(event):
    xx = await event.eor("**Lu Ngapah Begitu ?**")
    sleep(2)
    await xx.edit("**Keren Lu Begitu ?**")
