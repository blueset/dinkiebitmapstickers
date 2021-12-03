#%%
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from typing import Dict, List
from telethon.tl.types import StickerSet, InputStickerSetID
from telethon.tl.types.messages import StickerSet as StickerSetM
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
import asyncio
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed
import logging


logging.basicConfig(level=logging.DEBUG)

def retry_deco(fn):
    return AsyncRetrying(stop=stop_after_attempt(5), wait=wait_fixed(1)).wraps(fn)


load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client: TelegramClient = TelegramClient(
    "telethon", api_id, api_hash
)

#%%
mapping = {
    "a-baoquan": "🤜🤛",
    "a-handshake": "🤝",
    "a-heart": "❤️",
    "a-heartbreak": "💔",
    "a-heshi": "🙏",
    "a-like": "👍",
    "a-lips": "👄",
    "a-rose": "🌹",
    "a-rosewilted": "🥀",
    "f-emmm": "😑",
    "f-huaji": "😏",
    "f-laugh": "😁",
    "f-liekai": "🥴",
    "f-mask": "😷",
    "f-mindblow": "🤯",
    "f-pen": "🤤",
    "f-sad": "☹️",
    "f-scream": "😱",
    "f-shocked": "😲",
    "f-sigh": "😮‍💨",
    "f-smile": "🙂",
    "f-sweat": "😅",
    "f-tongue": "😝",
    "f-vomit": "🤮",
    "f-xiaoku": "😂",
    "f-xx": "😵",
    "g-ok": "👌",
    "g-yeah": "✌️",
    "n-crescent": "🌙",
    "n-doge": "🐶",
    "n-fish": "🐟",
    "n-lightning": "⚡",
    "n-pig": "🐷",
    "n-sparkle": "✨",
    "n-star": "🌟",
    "n-sun": "☀️",
    "n-turtle": "🐢",
    "p-birthday": "🎂",
    "o-bomb": "💣",
    "o-car": "🚗",
    "o-celebrate": "🎉",
    "o-knife": "🔪",
    "o-lightbulb": "💡",
    "o-loveletter": "💌",
    "o-pill": "💊",
    "o-pistol": "🔫",
    "o-present": "🎁",
    "o-shit": "💩",
    "o-skull": "💀",
    "z-18slash": "🔞",
    "z-100": "💯",
    "z-check": "✅",
    "z-cross": "❎",
    "z-de": "🉐",
    "z-ha": "🈴",
    "z-have": "🈶",
    "z-he": "🉑",
    "z-ke": "🉑",
    "z-nohave": "🈚️",
    "z-okbox": "🆗",

    # 0.11
    "2-lipu": "🍐🎼",
    "2-niupi": "🐄🍺",
    "f-heehee": "🤪",
    "f-pien": "🥺",
    "f-ziplip": "🥺",
    "n-cow": "🐄",
    "p-beer": "🍺",
    "p-cola": "🥤",
    "o-dice": "🎲",
    "o-game": "🎮",
    "o-guitar": "🎸",
    "o-music": "🎼",
    "o-musicnote": "🎵",
    "p-pear": "🍐",
    "o-robot": "🤖",
    "z-cool": "🆒",
    "z-hao": "👍",
    "z-qiang": "👍",
    "z-zan": "👍",

    # 0.12
    "g-handraise": "🙋",
    "g-nogood": "🙅",
    "g-shrug": "🤷",
    "f-kiss": "😘",

    "2-bullfrog": "🐮🐸",
    "2-byebye": "👋",
    "2-greeting": "🤝",
    "f-cry": "😭",
    "f-facepalm": "🤦",
    "f-farewell": "👋",
    "f-nerd": "🤓",
    "f-party": "🥳",
    "f-sneak": "🙈",  # New emoji, pending Telegram support: 🫣
    "f-wink": "😉",
    "n-frog": "🐸",
    "o-camera": "📷",
    "o-computer": "🖥️",
    "o-glasses": "👓",
    "o-save": "💾",
    "o-search": "🔍",
    "o-smartphone": "📱",
    "o-speak": "💬",
    "o-watch": "⌚",
    "p-coffee": "☕",
    "p-strawberry": "🍓",
    "p-watermelon": "🍉",

    # 0.2
    "3-congrats": "🎉🌹❤️",
    "f-meloneater": "🍉",
    "f-question": "❓",
    "f-zzz": "😴",
    "g-fist": "👊",
    "n-alien": "👽",
    "n-ghost": "👻",
    "n-horse": "🐴",
    "n-pigeon": "🕊️",
    "o-cellphone": "📱",
    "o-lowpower": "🔋",
    "o-plane": "✈️",
    "o-rocket": "🚀",
    "p-apple": "🍎",
    "p-banana": "🍌",
    "p-cake": "🍰",
    "p-cherry": "🍒",
    "p-hamburger": "🍔",
    "p-lemon": "🍋",
    "p-noodle": "🍜",
    "p-peach": "🍑",
    "p-rice": "🍚",
}

#%%
async def fetch_stickers() -> Dict[str, StickerSet]:
    sticker_sets = await client(GetAllStickersRequest(0))
    d = {}
    for s in sticker_sets.sets:
        d[s.short_name] = s
    return d

#%%
async def clear_pack(pack: StickerSet):
    full_pack: StickerSetM = await client(GetStickerSetRequest(stickerset=InputStickerSetID(
        id=pack.id, access_hash=pack.access_hash
    )))

    async with client.conversation("stickers", max_messages=100000) as conv:
        for doc in full_pack.documents:
            await retry_deco(conv.send_message)('/delsticker')
            await conv.get_response()
            await retry_deco(conv.send_message)(full_pack.set.short_name)
            await conv.get_response()
            await retry_deco(conv.send_file)(doc)
            await conv.get_response()

#%%
async def populate_pack(theme: str, pack: StickerSet):
    async with client.conversation("stickers", max_messages=100000) as conv:
        await conv.send_message('/addsticker')
        await conv.get_response()
        await conv.send_message(pack.short_name)
        await conv.get_response()
        for fn, emoji in sorted(mapping.items()):
            print(fn, emoji)
            await retry_deco(conv.send_file)(f"./output/{theme}/{fn}.png", force_document=True)
            await conv.get_response()
            await retry_deco(conv.send_message)(emoji)
            await conv.get_response()
        await conv.send_message("/done")
        await conv.get_response()


#%%
async def partial_populate_pack(theme: str, pack: StickerSet, keys: List[str]):
    async with client.conversation("stickers", max_messages=100000) as conv:
        await conv.send_message('/addsticker')
        await conv.get_response()
        await conv.send_message(pack.short_name)
        await conv.get_response()
        for fn in keys:
            emoji = mapping[fn]
            await retry_deco(conv.send_file)(f"./output/{theme}/{fn}.png", force_document=True)
            await conv.get_response()
            await retry_deco(conv.send_message)(emoji)
            await conv.get_response()
        await conv.send_message("/done")
        await conv.get_response()


#%%
async def update_pack(theme: str, pack: StickerSet):
    await clear_pack(pack)
    await populate_pack(theme, pack)

#%%
async def main():
    print("Starting...")
    # await client.start()
    async with client:
        print("Started")
        packs = await fetch_stickers()
        # await update_pack("light", packs["dinkie_light"])
        # await update_pack("dark", packs["dinkie_dark"])
        delta = [
            "2-lipu",
            "p-pear",
            "3-congrats",
            "f-meloneater",
            "f-question",
            "f-zzz",
            "g-fist",
            "n-alien",
            "n-ghost",
            "n-horse",
            "n-pigeon",
            "o-cellphone",
            "o-lowpower",
            "o-plane",
            "o-rocket",
            "p-apple",
            "p-banana",
            "p-cake",
            "p-cherry",
            "p-hamburger",
            "p-lemon",
            "p-noodle",
            "p-peach",
            "p-rice",
        ]
        await partial_populate_pack("dark", packs["dinkie_dark"], delta)
        await partial_populate_pack("light", packs["dinkie_light"], delta)

# %%
if __name__ == "__main__":
    asyncio.run(main())