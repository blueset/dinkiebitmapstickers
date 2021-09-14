#%%
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from typing import Dict
from telethon.tl.types import StickerSet, InputStickerSetID
from telethon.tl.types.messages import StickerSet as StickerSetM
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
import asyncio

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
    "f-kiss": "😘",
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
    "g-handraise": "🙋",
    "g-nogood": "🙅",
    "g-ok": "👌",
    "g-shrug": "🤷",
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
    "o-birthday": "🎂",
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

    async with client.conversation("stickers") as conv:
        for doc in full_pack.documents:
            await conv.send_message('/delsticker')
            await conv.get_response()
            await conv.send_message(full_pack.set.short_name)
            await conv.get_response()
            await conv.send_file(doc)
            await conv.get_response()

#%%
async def populate_pack(theme: str, pack: StickerSet):
    async with client.conversation("stickers") as conv:
        await conv.send_message('/addsticker')
        await conv.get_response()
        await conv.send_message(pack.short_name)
        await conv.get_response()
        for fn, emoji in mapping.items():
            await conv.send_file(f"./output/{theme}/{fn}.png", force_document=True)
            await conv.get_response()
            await conv.send_message(emoji)
            await conv.get_response()
        await conv.send_message("/done")
        await conv.get_response()


#%%
async def partial_populate_pack(theme: str, pack: StickerSet, start: str):
    keys = list(mapping.keys())
    idx = keys.index(start)
    async with client.conversation("stickers") as conv:
        for fn in keys[idx:]:
            emoji = mapping[fn]
            await conv.send_file(f"./output/{theme}/{fn}.png", force_document=True)
            await conv.get_response()
            await conv.send_message(emoji)
            await conv.get_response()
        await conv.send_message("/done")
        await conv.get_response()


#%%
async def update_pack(theme: str, pack: StickerSet):
    await clear_pack(pack)
    await populate_pack(theme, pack)

#%%
async def main():
    await client.start()
    packs = await fetch_stickers()
    await update_pack("light", packs["dinkie_light"])
    await update_pack("dark", packs["dinkie_dark"])

# %%
asyncio.run(main())