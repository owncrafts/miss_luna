import re
import os

from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=7364776,
    api_hash="76480e5d932eddfdc916d812eab9c3c2",
)

bot_id = int(bot_token.split(":")[0])
arq = None


async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )



async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")

#@luna.on_message(filters.command("calcy") & ~filters.edited)
  # async def exec(open("calcy.py").read())
  #  )


#@luna.on_message(filters.command("about") & ~filters.edited)
#async def repo(_, message):
#    await message.reply_text(
#        "**🔰 Developer information**\n\n**Name** : `Dhruv`\n**Full name** : `Dhruv Lathia`\n**Age** : `17`\n**Birthdate** : `30/04/2005`\n**Birthplace** : `India - Gujarat`\n**Education** : `Diploma Computer Engineering`\n**College** : `B & B Institute of Technology`\n**Instagram** : instagram.com/dhruv_lathia\n\n**Contact him for more info ⤵️**\n🔰 PM allowed - @dhruv_lathia 😇\n\nSend /community if you want to visit our all communities",
#       disable_web_page_preview=True,
#    )

@luna.on_message(filters.command("community") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("**🔰 Join our all communities**\n\n⬛️ Our all channels\n\n▫️ @CAPvsIRONMAN\n▫️ @DCvsMARVELchannel\n▫️ @Alpha_91\n\n⬛️ Our all groups\n\n▫️ @Movies_84\n▫️ @Moviesline_Official\n▫️ @Offtopic_Time\n⬛️ Our all Bots\n\n▫️ @MarvelCollectorBot\n▫️ @EmirichuBot\n▫️ @Levi_Chatbot\n▫️ @MovieslineBot\n▫️ @Buyads_Bot\n▫️ @Paidpromoz_Bot\n⬛️ Our all Websites\n\n▫️ www.filmmagik.rf.gd\n▫️ www.cyberer.xyz\n▫️ Special one coming soon...")


@luna.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("Hello, I am Luna. A User-friendly Chatbot. You can spend time on me & You can be my friend. My boyfriend is @dhruv_lathia, A person who coded me.")  



@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}luna[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
-----------------
| Luna Started! |
-----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
