import datetime
import pytz
from googletrans import Translator
from pyrogram import Client, filters
from pyrogram.types import Message
from soccer_data_api import SoccerDataAPI
from soccerapi.api import Api888Sport
from apscheduler.schedulers.asyncio import AsyncIOScheduler

soccer_data = SoccerDataAPI()
fixture_data = Api888Sport()
translator = Translator()


# Function to fetch fixture data for a specific league
def fetch_fixture(url_league: str) -> list:
    data = fixture_data.odds(url_league)
    return [{'home': i['home_team'], 'away': i['away_team'], 'time': i['time']} for i in data]


# List of important teams for upcoming games
importants_team = ['Paris SG', 'Monaco', 'Marseille', 'Lens', 'Rennes', 'FC Barcelona', 'Real Betis',
                   'Atlético Madrid', 'Real Madrid', 'Real Sociedad', 'Villarreal', 'Borussia Dortmund',
                   'Bayern Munich', '1. FC Union Berlin', 'RB Leipzig', 'SC Freiburg', 'Eintracht Frankfurt',
                   'Liverpool', 'Manchester United', 'Manchester City', 'Tottenham', 'Chelsea', 'Arsenal',
                   'Newcastle', 'Fulham', 'Brighton', 'Brentford', 'Inter', 'Inter AC Milan', 'Juventus', 'Lazio',
                   'Roma', 'Napoli', 'Atalanta']

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


# Function to check if a game is scheduled for today
async def is_game_today_checker(c: Client, m: Message, games_data):
    utc_timezone = pytz.timezone("UTC")
    local_timezone = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now()
    today_games_text = []
    emoji = "\U000023F0"
    for game in games_data:
        game_time = datetime.datetime.strptime(game['time'], '%Y-%m-%dT%H:%M:%SZ')
        utc_time = game_time.replace(tzinfo=utc_timezone)
        local_time = utc_time.astimezone(local_timezone)
        if local_time.date() == now.date():
            today_games_text.append(f"{game['home']} --- {game['away']}  \n {emoji}|{local_time.strftime('%H:%M')}")
    return today_games_text


async def is_game_today_checker_all_leagues(c: Client, m: Message, *games_data):
    utc_timezone = pytz.timezone("UTC")
    local_timezone = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now()
    today_games_text = []
    emoji = "\U000023F0"
    for league in games_data[0]:
        for game in league:
            game_time = datetime.datetime.strptime(game['time'], '%Y-%m-%dT%H:%M:%SZ')
            utc_time = game_time.replace(tzinfo=utc_timezone)
            local_time = utc_time.astimezone(local_timezone)
            if local_time.date() == now.date():
                today_games_text.append(f"{game['home']} vs {game['away']}  \n {emoji}|{local_time.strftime('%H:%M')}")
    return today_games_text


async def is_game_today_checker_all_leagues_predection(c: Client, m: Message, *games_data):
    utc_timezone = pytz.timezone("UTC")
    local_timezone = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now()
    today_games_text = []
    emoji = "\U000023F0"
    for league in games_data[0]:
        for game in league:
            game_time = datetime.datetime.strptime(game['time'], '%Y-%m-%dT%H:%M:%SZ')
            utc_time = game_time.replace(tzinfo=utc_timezone)
            local_time = utc_time.astimezone(local_timezone)
            if local_time.date() == now.date():
                today_games_text.append(f"{game['home']} -- {game['away']}  \n {emoji}|{local_time.strftime('%H:%M')}")
    return today_games_text


# Function to send upcoming games for today
async def send_upcoming_games(c: Client, m: Message, league):
    today_games_text = await is_game_today_checker(c, m, league)
    if today_games_text:
        for game in today_games_text:
            # today_games_text_persian = translator.translate(str(game), dest='fa')
            formatted_games = game
            await m.reply_text(formatted_games)
    else:
        await m.reply_text('امروز در این لیگ بازی برگذار نمی شود')


async def send_upcoming_games_all_leagues(c: Client, m: Message, *league):
    today_games_text = await is_game_today_checker_all_leagues(c, m, league)
    if today_games_text:
        for game in today_games_text:
            # today_games_text_persian = translator.translate(str(game), dest='fa')
            formatted_games = game
            await m.reply_text(formatted_games)
    else:
        await m.reply_text('امروز در این لیگ بازی برگذار نمی شود')


# Function to check if any important games are scheduled for today
async def is_important_games(c: Client, m: Message, *league):
    important_teams = importants_team
    today_games_text = await is_game_today_checker_all_leagues_predection(c, m, league)
    important_games = []
    for team in important_teams:
        for game in today_games_text:
            if team in game:
                if game not in important_games:
                    important_games.append(game)
    if important_games:
        for game in important_games:
            # today_games_text_persian = translator.translate(str(game), dest='fa')
            formatted_games = game
            await m.reply_text(formatted_games)
    else:
        await m.reply_text('هیچ بازی ای در برنامه امروز کانال های ییش بینی قرار ندارد')


# Define message handlers for different leagues
@Client.on_message(filters.regex('برنامه امروز سی ال'))
async def send_today_ucl_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, Ucl_fixture)


@Client.on_message(filters.regex('برنامه امروز ای ال'))
async def send_today_uel_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, Uel_fixture)


@Client.on_message(filters.regex('برنامه امروز اسپانیا'))
async def send_today_spain_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, LaLiga_fixture)


@Client.on_message(filters.regex('برنامه امروز حذفی اسپانیا'))
async def send_today_spain_copa_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, CopaDelRey_fixture)


@Client.on_message(filters.regex('برنامه امروز ایتالیا'))
async def send_today_italy_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, SERIEA_fixture)


@Client.on_message(filters.regex('برنامه امروز حذفی ایتالیا'))
async def send_today_italy_copa_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, CoppaItalia_fixture)


@Client.on_message(filters.regex('برنامه امروز المان'))
async def send_today_germany_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, Bundesliga_fixture)


@Client.on_message(filters.regex('برنامه امروز حذفی المان'))
async def send_today_germany_copa_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, DFBPokal_fixture)


@Client.on_message(filters.regex('برنامه امروز انگلیس'))
async def send_today_england_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, PremierLeague_fixture)


@Client.on_message(filters.regex('برنامه امروز حذفی انگلیس'))
async def send_today_england_copa_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, FACup_fixture)


@Client.on_message(filters.regex('برنامه امروز فرانسه'))
async def send_today_france_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, Ligue1_fixture)


@Client.on_message(filters.regex('برنامه امروز حذفی فرانسه'))
async def send_today_france_copa_fixture(c: Client, m: Message):
    await send_upcoming_games(c, m, CoupedeFrance_fixture)


@Client.on_message(filters.regex('برنامه امروز'))
async def send_today_all_games_fixture(c: Client, m: Message):
    await send_upcoming_games_all_leagues(c, m, LaLiga_fixture, CopaDelRey_fixture, Ligue1_fixture, CoppaItalia_fixture,
                                          Bundesliga_fixture, DFBPokal_fixture, PremierLeague_fixture, FACup_fixture,
                                          SERIEA_fixture, CoppaItalia_fixture, Ucl_fixture, Uel_fixture)


@Client.on_message(filters.regex('برنامه پیش بینی'))
async def send_today_all_games_important_fixture(c: Client, m: Message):
    await is_important_games(c, m, LaLiga_fixture, CopaDelRey_fixture, Ligue1_fixture, CoppaItalia_fixture,
                             Bundesliga_fixture, DFBPokal_fixture, PremierLeague_fixture, FACup_fixture,
                             SERIEA_fixture, CoppaItalia_fixture, Ucl_fixture, Uel_fixture)


# scheduler = AsyncIOScheduler()
# scheduler.add_job(send_today_spain_fixture, "interval", seconds=3600)
# scheduler.start()

print('Upcoming module loaded.')

