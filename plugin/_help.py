# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from telethon.errors.rpcerrorlist import (
    BotInlineDisabledError,
    BotMethodInvalidError,
    BotResponseTimeoutError,
)
from telethon.tl.custom import Button

from Lutpan.dB._core import HELP, LIST
from Lutpan.fns.tools import cmd_regex_replace

from . import HNDLR, LOGS, OWNER_NAME, asst, kazu_cmd, get_string, inline_pic, udB

_main_help_menu = [
    [
        Button.inline(get_string("help_4"), data="uh_Official_"),
        Button.inline(get_string("help_5"), data="uh_Addons_"),
    ],
    [Button.inline(get_string("help_10"), data="close")],
]


@lutpan_cmd(pattern="help( (.*)|$)")
async def _help(lutpan):
    plug = lutpan.pattern_match.group(1).strip()
    chat = await lutpan.get_chat()
    if plug:
        try:
            if plug in HELP["Official"]:
                output = f"**Plugin** - `{plug}`\n"
                for i in HELP["Official"][plug]:
                    output += i
                output += "\n◈ ᴋᴀᴢᴜ ᴜʙᴏᴛ"
                await lutpan.eor(output)
            elif HELP.get("Addons") and plug in HELP["Addons"]:
                output = f"**Plugin** - `{plug}`\n"
                for i in HELP["Addons"][plug]:
                    output += i
                output += "\n〄 ʟᴜᴛᴘᴀɴ ᴜʙᴏᴛ"
                await lutpan.eor(output)
            else:
                try:
                    x = get_string("help_11").format(plug)
                    for d in LIST[plug]:
                        x += HNDLR + d
                        x += "\n"
                    x += "\n◈ ʟᴜᴛᴘᴀɴ ᴜʙᴏᴛ"
                    await kazu.eor(x)
                except BaseException:
                    file = None
                    compare_strings = []
                    for file_name in LIST:
                        compare_strings.append(file_name)
                        value = LIST[file_name]
                        for j in value:
                            j = cmd_regex_replace(j)
                            compare_strings.append(j)
                            if j.strip() == plug:
                                file = file_name
                                break
                    if not file:
                        # the enter command/plugin name is not found
                        text = f"`{plug}` is not a valid plugin!"
                        if best_match := next(
                            (
                                _
                                for _ in compare_strings
                                if plug in _ and not _.startswith("_")
                            ),
                            None,
                        ):
                            text += f"\nDid you mean `{best_match}`?"
                        return await lutpan.eor(text)
                    output = f"**Command** `{plug}` **found in plugin** - `{file}`\n"
                    if file in HELP["Official"]:
                        for i in HELP["Official"][file]:
                            output += i
                    elif HELP.get("Addons") and file in HELP["Addons"]:
                        for i in HELP["Addons"][file]:
                            output += i
                    output += "\n◈ ʟᴜᴛᴘᴀɴ ᴜʙᴏᴛ"
                    await kazu.eor(output)
        except BaseException as er:
            LOGS.exception(er)
            await kazu.eor("Error 🤔 occured.")
    else:
        try:
            results = await lutpan.client.inline_query(asst.me.username, "lutpan")
        except BotMethodInvalidError:
            z = []
            for x in LIST.values():
                z.extend(x)
            cmd = len(z) + 10
            if udB.get_key("MANAGER") and udB.get_key("DUAL_HNDLR") == "/":
                _main_help_menu[2:2] = [[Button.inline("• Manager Help •", "mngbtn")]]
            return await lutpan.reply(
                get_string("inline_4").format(
                    OWNER_NAME,
                    len(HELP["Official"]),
                    len(HELP["Addons"] if "Addons" in HELP else []),
                    cmd,
                ),
                file=inline_pic(),
                buttons=_main_help_menu,
            )
        except BotResponseTimeoutError:
            return await lutpan.eor(
                get_string("help_2").format(HNDLR),
            )
        except BotInlineDisabledError:
            return await lutpan.eor(get_string("help_3"))
        await results[0].click(chat.id, reply_to=lutpan.reply_to_msg_id, hide_via=True)
        await lutpan.delete()
