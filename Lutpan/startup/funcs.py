# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import asyncio
import os, shutil
import random
import time
from random import randint

try:
    from pytz import timezone
except ImportError:
    timezone = None

from telethon.errors import (
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (CreateChannelRequest,
                                            EditAdminRequest, EditPhotoRequest,
                                            InviteToChannelRequest,
                                            JoinChannelRequest)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id

from .. import LOGS, LutpanConfig
from ..fns.helper import download_file, inline_mention, updater

db_url = 0


async def autoupdate_local_database():
    from .. import asst, udB, kazu_bot, Var

    global db_url
    if db_url := (
        udB.get_key("TGDB_URL")
        or Var.TGDB_URL
        or kazu_bot._cache.get("TGDB_URL")
    ):
        _split = db_url.split("/")
        _channel = _split[-2]
        _id = _split[-1]
        try:
            await asst.edit_message(
                int(_channel) if _channel.isdigit() else _channel,
                message=_id,
                file="database.json",
                text="**Do not delete this file.**",
            )
        except MessageNotModifiedError:
            return
        except MessageIdInvalidError:
            pass
    try:
        LOG_CHANNEL = (
            udB.get_key("LOG_CHANNEL")
            or Var.LOG_CHANNEL
            or asst._cache.get("LOG_CHANNEL")
            or "me"
        )
        msg = await asst.send_message(
            LOG_CHANNEL, "**Do not delete this file.**", file="database.json"
        )
        asst._cache["TGDB_URL"] = msg.message_link
        udB.set_key("TGDB_URL", msg.message_link)
    except Exception as ex:
        LOGS.error(f"Error on autoupdate_local_database: {ex}")


def update_envs():
    """Update Var. attributes to udB"""
    from .. import udB

    for envs in list(os.environ):
        if envs in ["LOG_CHANNEL", "BOT_TOKEN"] or envs in udB.keys():
            udB.set_key(envs, os.environ[envs])


async def join_ajg():
    import sys

    from telethon.errors import rpcerrorlist

    from .. import lutpan_bot

    try:
        await lutpan_bot(JoinChannelRequest("kynansupport"))
        await lutpan_bot(JoinChannelRequest("KazuSupportGrp"))
    except rpcerrorlist.ChannelPrivateError:
        print(
            "Lu Di Ban Di @KazuSupportGrp atau @kynansupport Jadi Ga Bisa Pake Bot Ini ! Minta Unban Dulu Sana."
        )
        sys.exit(1)

async def startup_stuff():
    from .. import udB

    x = ["resources/auth", "resources/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    if CT := udB.get_key("CUSTOM_THUMBNAIL"):
        path = "resources/extras/thumbnail.jpg"
        KazuConfig.thumb = path
        try:
            await download_file(CT, path)
        except Exception as er:
            LOGS.exception(er)
    elif CT is False:
        KazuConfig.thumb = None
    if GT := udB.get_key("GDRIVE_AUTH_TOKEN"):
        with open("resources/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if udB.get_key("AUTH_TOKEN"):
        udB.del_key("AUTH_TOKEN")

    MM = udB.get_key("MEGA_MAIL")
    MP = udB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = udB.get_key("TIMEZONE")
    if TZ and timezone:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.debug(er)
        except BaseException:
            LOGS.critical(
                "Zona waktu salah"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import udB, lutpan_bot

    if udB.get_key("BOT_TOKEN"):
        return
    await lutpan_bot.start()
    LOGS.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    who = lutpan_bot.me
    name = f"{who.first_name}' Bot"
    if who.username:
        username = f"{who.username}_bot"
    else:
        username = f"lutpan_{str(who.id)[5:]}_bot"
    bf = "@BotFather"
    await lutpan_bot(UnblockRequest(bf))
    await lutpan_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await lutpan_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await lutpanb_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do.") or "20 bots" in isdone:
        LOGS.critical(
            "Tolong buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan mulai ulang saya."
        )
        import sys

        sys.exit(1)
    await lutpan_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await lutpan_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await lutpan_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await lutpan_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.critical(
                "Tolong buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan mulai ulang saya."
            )
            import sys

            sys.exit(1)
    await lutpan_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await lutpan_bot.get_messages(bf, limit=1))[0].text
    await kazu_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"lutpan_{str(who.id)[6:]}{ran}_bot"
        await kazu_bot.send_message(bf, username)
        await asyncio.sleep(1)
        isdone = (await lutpan_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set_key("BOT_TOKEN", token)
        await enable_inline(lutpan_bot, username)
        LOGS.info(
            f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
        )
    else:
        LOGS.info(
            "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, udB, kazu_bot

    channel = udB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await lutpan_bot.get_entity(channel)
        except BaseException as err:
            LOGS.exception(err)
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:

        async def _save(exc):
            udB._cache["LOG_CHANNEL"] = Lutpan_bot.me.id
            await asst.send_message(
                Lutpan_bot.me.id, f"Gagal Membuat Saluran Log karena {exc}.."
            )

        if lutpan_bot._bot:
            msg_ = "'LOG_CHANNEL' tidak ditemukan! Tambahkan untuk digunakan 'BOTMODE'"
            LOGS.error(msg_)
            return await _save(msg_)
        LOGS.info("Membuat Saluran Log untuk Anda!")
        try:
            r = await lutpan_bot(
                CreateChannelRequest(
                    title="Logs Lutpan Ubot",
                    about="Logs Lutpan Ubot \n\n Cʀᴇᴀᴛᴇᴅ Bʏ @kazusupportgrp",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError as er:
            LOGS.critical(
                "Anda Berada di Terlalu Banyak Saluran & Grup, Tinggalkan beberapa dan Mulai Ulang Bot"
            )
            return await _save(str(er))
        except BaseException as er:
            LOGS.exception(er)
            LOGS.info(
                "Ada yang Salah, Buat Grup dan atur idnya di config var LOG_CHANNEL."
            )

            return await _save(str(er))
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", channel)
    assistant = True
    try:
        await lutpan_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await lutpan_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("Kesalahan saat Menambahkan Asisten ke Saluran Log")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("Terjadi error saat mendapatkan saluran Log dari Asisten")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await lutpan_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Gagal mempromosikan 'Bot Asisten' di 'Log Channel' karena 'Hak Istimewa Admin'"
                )
            except BaseException as er:
                LOGS.info("Terjadi kesalahan saat mempromosikan asisten di Log Channel..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo = await download_file(
            "https://graph.org//file/d854abd533a783c6642b1.jpg",
            "resources/extras/logo.jpg",
        )
        ll = await lutpan_bot.upload_file(photo)
        try:
            await lutpan_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, udB, lutpan_bot

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("Menyesuaikan Bot Asisten di @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not kazu_bot.me.username:
            sir = kazu_bot.me.first_name
        else:
            sir = f"@lutpan_bot.me.username}"
        file = random.choice(
            [
                "https://graph.org//file/d854abd533a783c6642b1.jpg",
                "resources/extras/logo.jpg",
            ]
        )
        if not os.path.exists(file):
            file = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Penyesuaian Otomatis** Dimulai @Botfather"
        )
        await asyncio.sleep(1)
        await lutpan_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await lutpan_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await lutpan_bot.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGS.info("Error while trying to customise assistant, skipping...")
            return
        await lutpan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await lutpan_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await lutpan_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await lutpan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await lutpan_bot.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await lutpan_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await lutpan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await lutpan_bot.send_message(
            "botfather",
            f"✨ Powerful Kazu Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @KazuSupportGrp ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("Completed **Auto Customisation** at @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import lutpan_bot
    from .utils import load_addons

    if lutpan_bot._bot:
        LOGS.info("Plugin Channels can't be used in 'BOTMODE'")
        return
    if os.path.exists("addons") and not os.path.exists("addons/.git"):
        shutil.rmtree("addons")
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = lutpan_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in lutpan_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = "addons/" + x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(plugin):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(plugin)
                try:
                    load_addons(plugin)
                except Exception as e:
                    LOGS.info(f"Lutpan - PLUGIN_CHANNEL - ERROR - {plugin}")
                    LOGS.exception(e)
                    os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs


async def ready():
    from .. import asst, udB, lutpan_bot
    from ..fns.tools import async_searcher

    chat_id = udB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not udB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """ **Thanks for Deploying Lutpan Ubot!**
• Here, are the Some Basic stuff from, where you can Know, about its Usage."""
        PHOTO = "https://graph.org//file/97b753a248f764d72d47c.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        udB.set_key("INIT_DEPLOY", "Done")
    else:
        MSG = f"**Lutpan Ubot has been deployed!**\n➖➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(kazu_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**Support**: @kazusupportgrp\n➖➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        if prev_spam := udB.get_key("LAST_UPDATE_LOG_SPAM"):
            try:
                await lutpan_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info(f"Kesalahan saat Menghapus Pesan Pembaruan Sebelumnya :{str(E)}")
        if await updater():
            BTTS = Button.inline("Pembaruan tersedia", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await lutpan_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await lutpan_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    if spam_sent and not spam_sent.media:
        udB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    get_ = udB.get_key("OLDANN") or []
    try:
        updts = await async_searcher(
            "https://ultroid-api.vercel.app/announcements", post=True, re_json=True
        )
        for upt in updts:
            key = list(upt.keys())[0]
            if key not in get_:
                cont = upt[key]
                if isinstance(cont, str):
                    await asst.send_message(chat_id, cont)
                elif isinstance(cont, dict) and cont.get("chat"):
                    await asst.forward_messages(chat_id, cont["msg_id"], cont["chat"])
                else:
                    LOGS.info(cont)
                    LOGS.info(
                        "Invalid Type of Announcement Detected!\nMake sure you are on latest version.."
                    )
                get_.append(key)
        udB.set_key("OLDANN", get_)
    except Exception as er:
        LOGS.exception(er)


async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, kazu_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else kazu_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__Restarted Successfully.__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)


async def enable_inline(lutpan_bot, username):
    bf = "BotFather"
    await lutpan_bot.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await lutpan_bot.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await lutpan_bot.send_message(bf, "Search")
    await lutpan_bot.send_read_acknowledge(bf)
