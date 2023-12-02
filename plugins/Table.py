from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import Message
from soccer_data_api import SoccerDataAPI
from soccerapi.api import Api888Sport

soccer_data = SoccerDataAPI()
fixture_data = Api888Sport()
translator = Translator()


# Function to fetch league table data
def fetch_table(league: str) -> list:
    data = soccer_data.__getattribute__(league)()
    return [{'team': i['team'], 'points': i['points']} for i in data]
    # return [i['team'] and f['points'] for i, f in data]


# Define tables for various leagues
england_table = fetch_table('english_premier')
spain_table = fetch_table('la_liga')
france_table = fetch_table('ligue_1')
germany_table = fetch_table('bundesliga')
italy_table = fetch_table('serie_a')


# Function to send table information in a formatted way
async def send_table(c: Client, m: Message, table: list):
    text = "\n".join([f"{i + 1}- {table[i]['team']} {table[i]['points']}" for i in range(len(table))])
    # text_tr = translator.translate(str(text), dest='fa') [note : this translator lib isn't working anymore]
    await c.send_message(chat_id=m.chat.id, text=text)


# Define message handlers for different leagues
@Client.on_message(filters.regex('جدول انگلیس'))
async def sender_england(c: Client, m: Message):
    await send_table(c, m, england_table)


@Client.on_message(filters.regex('سلام'))
async def response(self, m: Message):
    print('hi')


@Client.on_message(filters.regex('جدول اسپانیا'))
async def sender_spain(c: Client, m: Message):
    await send_table(c, m, spain_table)


@Client.on_message(filters.regex('جدول فرانسه'))
async def sender_france(c: Client, m: Message):
    await send_table(c, m, france_table)


@Client.on_message(filters.regex('جدول آلمان'))
async def sender_germany(c: Client, m: Message):
    await send_table(c, m, germany_table)


@Client.on_message(filters.regex('جدول ایتالیا'))
async def sender_italy(c: Client, m: Message):
    await send_table(c, m, italy_table)


print('Table module loaded.')
