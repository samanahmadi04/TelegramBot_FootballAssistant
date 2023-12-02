from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import Message
from soccer_data_api import SoccerDataAPI
from soccerapi.api import Api888Sport

soccer_data = SoccerDataAPI()
fixture_data = Api888Sport()
translator = Translator()


# Function to fetch fixture data for a specific league
def fetch_fixture(url_league: str) -> list:
    data = fixture_data.odds(url_league)
    return [{'home': i['home_team'], 'away': i['away_team'], 'time': i['time']} for i in data]


# Define fixture URLs for various leagues
Ucl_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/champions_league/')
Uel_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/europa_league/')
SERIEA_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/italy/serie_a/')
PremierLeague_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/england/premier_league/')
Bundesliga_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/germany/bundesliga/')
LaLiga_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/spain/la_liga/')
Ligue1_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/france/ligue_1/')
CopaDelRey_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/spain/copa_del_rey/')
CoppaItalia_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/italy/coppa_italia/')
FACup_fixture = fetch_fixture("https://www.888sport.com/#/filter/football/england/fa_cup/")
DFBPokal_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/germany/dfb_pokal/')
CoupedeFrance_fixture = fetch_fixture('https://www.888sport.com/#/filter/football/france/coupe_de_france/')


# Function to send fixture information in a formatted way
async def send_fixture(c: Client, m: Message, fixture):
    text = "\n".join([f"{i + 1}- {fixture[i]['home']}  -  {fixture[i]['away']}" for i in range(len(fixture))])
    # text_tr = translator.translate(str(text), dest='fa') [note : this translator lib isn't working anymore]
    await m.reply_text(text)


# Define message handlers for different leagues
@Client.on_message(filters.regex('برنامه سی ال'))
async def send_ucl_fixture(client: Client, message: Message):
    await send_fixture(client, message, Ucl_fixture)


@Client.on_message(filters.regex('برنامه ای ال'))
async def send_uel_fixture(client: Client, message: Message):
    await send_fixture(client, message, Uel_fixture)


@Client.on_message(filters.regex('برنامه ایتالیا'))
async def send_seriea_fixture(client: Client, message: Message):
    await send_fixture(client, message, SERIEA_fixture)


@Client.on_message(filters.regex('برنامه حذفی ایتالیا'))
async def send_CoppaItalia_fixture(client: Client, message: Message):
    await send_fixture(client, message, CoppaItalia_fixture)


@Client.on_message(filters.regex('برنامه انگلیس'))
async def send_premierleague_fixture(client: Client, message: Message):
    await send_fixture(client, message, PremierLeague_fixture)


@Client.on_message(filters.regex('برنامه حذفی انگلیس'))
async def send_FACup_fixture(client: Client, message: Message):
    await send_fixture(client, message, FACup_fixture)


@Client.on_message(filters.regex('برنامه المان'))
async def send_bundesliga_fixture(client: Client, message: Message):
    await send_fixture(client, message, Bundesliga_fixture)


@Client.on_message(filters.regex('برنامه حذفی المان'))
async def send_DFBPokal_fixture(client: Client, message: Message):
    await send_fixture(client, message, DFBPokal_fixture)


@Client.on_message(filters.regex('برنامه اسپانیا'))
async def send_laliga_fixture(client: Client, message: Message):
    await send_fixture(client, message, LaLiga_fixture)


@Client.on_message(filters.regex('برنامه حذفی اسپانیا'))
async def send_CopaDelRey_fixture(client: Client, message: Message):
    await send_fixture(client, message, CopaDelRey_fixture)


@Client.on_message(filters.regex('برنامه فرانسه'))
async def send_league1_fixture(client: Client, message: Message):
    await send_fixture(client, message, Ligue1_fixture)


@Client.on_message(filters.regex('برنامه حذفی فرانسه'))
async def send_CoupedeFrance_fixture(client: Client, message: Message):
    await send_fixture(client, message, CoupedeFrance_fixture)


print("Fixture module loaded.")
