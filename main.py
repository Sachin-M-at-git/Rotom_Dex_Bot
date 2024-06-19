import asyncio
import os
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from quart import Quart, request
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, ForceReply, InlineKeyboardMarkup, \
    InlineKeyboardButton


load_dotenv()
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

web_app = Quart(__name__)

app = Client(
    "RotomDexBot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)


@app.on_message(filters.command('start'))
async def start(app, message):
    await app.send_message(
        message.chat.id,
        "Welcome!",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Go Inline 🌐",
                                      switch_inline_query_current_chat="Pikachu"
                                      )
                 ]
            ])
    )


@app.on_inline_query()
def inline_query(app, inline_query):
    print(inline_query.query)
    response = requests.get(f'https://pokemon-api-six-tau.vercel.app/pokemon/{inline_query.query}')
    if response.status_code == 200:
        # Convert the response JSON data to a Python dictionary
        poke_d = response.json()
        print(poke_d)
        line_1 = ('═' * 26) if str(inline_query.chat_type) == 'ChatType.PRIVATE' else ('═' * 22)
        line_2 = ('➖' * 16) if str(inline_query.chat_type) == 'ChatType.PRIVATE' else ('➖' * 13)
        abilities = ""
        for ability in poke_d['Pokédex data']['Abilities']:
            abilities += f"<blockquote>**__Name__** : {ability['name']}\n**__Effect__** : {ability['effect']}\n{'__(hidden ability)__' if ability['hidden'] else ''}</blockquote>"
        pokemon_data = (
            f"{line_1}\n[🔖]({poke_d['Pokédex data']['image']['large_img']}) **{poke_d['Pokédex data']['name'].upper()}**\n{line_1}\n"
            f"⦾ 𝙋𝙊𝙆𝙀𝙈𝙊𝙉 𝘿𝘼𝙏𝘼:\n\n"
            f"⦿ **National No:** {poke_d['Pokédex data']['National No']}\n"
            f"⦿ **Type:** {', '.join(poke_d['Pokédex data']['Type'])}\n"
            f"⦿ **Species:** {poke_d['Pokédex data']['Species']}\n"
            f"⦿ **Height:** {poke_d['Pokédex data']['Height']}\n"
            f"⦿ **Weight:** {poke_d['Pokédex data']['Weight']}\n\n"
            f"⦿ **Abilities:**\n{abilities}\n{line_2}\n"
            f"⦾ 𝙏𝙍𝘼𝙄𝙉𝙄𝙉𝙂 𝘿𝘼𝙏𝘼:\n\n"
            f"⦿ **EV yield:** {poke_d['Training']['EV yield']}\n"
            f"⦿ **Catch rate:** {poke_d['Training']['Catch rate']}\n"
            f"⦿ **Base Friendship:** {poke_d['Training']['Base Friendship']}\n"
            f"⦿ **Base Exp:** {poke_d['Training']['Base Exp.']}\n"
            f"⦿ **Growth Rate:** {poke_d['Training']['Growth Rate']}\n{line_2}\n"
        )
        inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    thumb_url=poke_d['Pokédex data']['image']['small_img'],
                    title=poke_d['Pokédex data']['name'] + ' #' + str(poke_d['Pokédex data']['National No']),
                    description=f"Type: {', '.join(poke_d['Pokédex data']['Type'])}",
                    input_message_content=InputTextMessageContent(
                        f"{pokemon_data}"
                    )
                )
            ],
            cache_time=1
        )


@app.on_message(filters.command('find'))
async def find(app, message):
    global pokemon_data
    print(message.command[1:])
    poke = ' '.join(message.command[1:])
    # Send a GET request to the API
    response = requests.get(f'https://pokemon-api-six-tau.vercel.app/pokemon/{poke}')
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response JSON data to a Python dictionary
        poke_d = response.json()
        print(poke_d)
        line_1 = ('═' * 26) if str(message.chat.type) == 'ChatType.PRIVATE' else ('═' * 22)
        line_2 = ('➖' * 16) if str(message.chat.type) == 'ChatType.PRIVATE' else ('➖' * 13)
        abilities = ""
        for ability in poke_d['Pokédex data']['Abilities']:
            abilities += f"<blockquote>**__Name__** : {ability['name']}\n**__Effect__** : {ability['effect']}\n{'__(hidden ability)__' if ability['hidden'] else ''}</blockquote>"
            pokemon_data = (f"{line_1}\n**{poke_d['Pokédex data']['name']}**\n{line_1}\n"
                            f"⦾ 𝙋𝙊𝙆𝙀𝙈𝙊𝙉 𝘿𝘼𝙏𝘼:\n\n"
                            f"⦿ **National No:** {poke_d['Pokédex data']['National No']}\n"
                            f"⦿ **Type:** {', '.join(poke_d['Pokédex data']['Type'])}\n"
                            f"⦿ **Species:** {poke_d['Pokédex data']['Species']}\n"
                            f"⦿ **Height:** {poke_d['Pokédex data']['Height']}\n"
                            f"⦿ **Weight:** {poke_d['Pokédex data']['Weight']}\n\n"
                            f"⦿ **Abilities:**\n{abilities}\n{line_2}\n"
                            f"⦾ 𝙏𝙍𝘼𝙄𝙉𝙄𝙉𝙂 𝘿𝘼𝙏𝘼:\n\n"
                            f"⦿ **EV yield:** {poke_d['Training']['EV yield']}\n"
                            f"⦿ **Catch rate:** {poke_d['Training']['Catch rate']}\n"
                            f"⦿ **Base Friendship:** {poke_d['Training']['Base Friendship']}\n"
                            f"⦿ **Base Exp:** {poke_d['Training']['Base Exp.']}\n"
                            f"⦿ **Growth Rate:** {poke_d['Training']['Growth Rate']}\n{line_2}\n"
                            )
        await app.send_photo(
            message.chat.id,
            photo=await make_square(poke_d['Pokédex data']['image']['large_img']),
            caption=pokemon_data
        )
    else:
        await app.send_message(message.chat.id, "```\nNo Pokémon entry found! Zzt-zzt!\n```")


async def make_square(image_url):
    # Download the image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Calculate the size of the new square image
    max_dimension = max(img.size)

    # Create a new image with white background
    new_img = Image.new("RGB", (max_dimension, max_dimension), (255, 255, 255))

    # Calculate the position to paste the original image on the new image
    paste_position = ((max_dimension - img.width) // 2, (max_dimension - img.height) // 2)

    # Paste the original image onto the new image
    new_img.paste(img, paste_position)

    # Save the new image to a BytesIO object
    output = BytesIO()
    new_img.save(output, format="JPEG")
    output.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    return output


@web_app.route('/webhook', methods=['POST'])
async def handle_webhook():
    update = await request.get_json()
    await app.process_update(update)
    return "OK"


async def run_pyrogram():
    await app.start()
    print("I AM ALIVE")
    print("Started")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_pyrogram())
    web_app.run(loop=loop, host="127.0.0.1", port=8000)
