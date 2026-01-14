import discord
from discord import app_commands
from discord.ext import commands
import requests
import random
from typing import Optional
import math
from datetime import datetime, timezone
import unicodedata

# A kód a Discord bot időjárási funkcióit valósítja meg magyar nyelven.
# Ez a program a OpenWeatherMap API-t használja az időjárási adatok lekérésére,
# és különböző parancsokat biztosít a felhasználók számára, mint például időjárás lekérdezése,
# városok összehasonlítása, legmelegebb/leghidegebb város keresése, öltözködési tanácsok stb.

# Ez a program Apache Licence 2.0 licenc alatt áll.

# Licenc weboldala: https://www.apache.org/licenses/LICENSE-2.0

# --- CONFIGURATION ---
# WARNING: These keys are now hardcoded in the script.
# This is a security risk if the code is shared publicly.
DISCORD_TOKEN = "#"  # Replace with your valid Discord bot token
WEATHER_API_KEY = "#"  # Replace with your valid OpenWeatherMap API key
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of major Hungarian cities (you can expand this list!)
HUNGARIAN_CITIES = [
    "Budapest", "Debrecen", "Szeged", "Miskolc", "Pecs", "Gyor", "Nyiregyhaza", "Kecskemet", 
    "Szekesfehervar", "Szombathely", "Eger", "Tatabanya", "Sopron", "Veszprem", "Bekescsaba", 
    "Zalaegerszeg", "Erd", "Kaposvar", "Salgotarjan", "Dunaujvaros", "Papa", "Varpalota", 
    "Hodmezovasarhely", "Cegled", "Nagykata", "Jaszbereny", "Baja", "Szolnok", "Vac", 
    "Szigetszentmiklos", "Budaors", "Vecses", "Kiskunfelegyhaza", "Fuzesabony", "Morahalom", 
    "Oroszlany", "Tata", "Kiskunhalas", "Torokbalint", "Vamosgyork", "Szigetvar", "Komarom", 
    "Sarbogard", "Ajka", "Csopak", "Balatonfured", "Tihany", "Siofok", "Keszthely", 
    "Vonyarcvashegy", "Zamardi", "Pecsely", "Felsoors", "Balatonalmadi", "Balatonkenese", 
    "Alsoors", "Revfulop", "Balatongyorok", "Vaszolyi", "Koroshegy", "Paloznak", "Vors", 
    "Zanka", "Szentendre", "Visegrad", "Dunakeszi", "Szazhalombatta", "Szigethalom", "Sarvar", 
    "Lenti", "Szekszard", "Kunszentmarton", "Nagykoros", "Pecsvarad", "Godollo", "Tapioszecso", 
    "Kisvarda", "Paks", "Nagyszenas", "Szilvasvarad", "Kiskunlachaza", "Lajosmizse", 
    "Berettyoujfalu", "Sopronkovesd", "Miklosi", "Mindszent", "Nyirbator", "Ozd", "Kesznyeten", 
    "Mateszalka", "Szarvas", "Zsambek", "Bonyhad", "Kunsziget", "Rackeve", "Koka", "Heviz", 
    "Hevizgyork", "Tornyospalca", "Szentlorinc", "Vasarosnameny", "Ketpo", "Lajoskomarom", 
    "Szentgotthard", "Buk", "Kormend", "Pilisvorosvar", "Sarisap", "Csakvar", "Kolesd", 
    "Nagykanizsa", "Fertod", "Fertoszentmiklos", "Alsopeteny", "Per", "Szecseny",
    "Holloko", "Mezokovesd", "Tokaj", "Satoraljaujhely", "Szerencs", "Sarospatak", 
    "Koszeg", "Szigetmonostor", "Pomaz", "Budakalasz", "Solymar", "Biatorbagy", 
    "Telki", "Piliscsaba", "Veresegyhaz", "Fot", "Gyomro", "Monor", "Dabas", 
    "Rackeve", "Kalocsa", "Mohacs", "Szigetvar", "Harkany", "Villany", "Siklos", 
    "Szigliget", "Badacsonytomaj", "Abrahamhegy", "Fonyod", "Balatonlelle", 
    "Balatonboglar", "Balatonszarszo", "Balatonszemes", "Balatonbereny", "Heviz", 
    "Kehidakustany", "Zalakaros", "Tapolca", "Sumeg", "Herend", "Zirc", 
    "Pannonhalma", "Lebeny", "Mosonmagyarovar", "Rajka", "Hegyeshalom"
]

# Game state management: {channel_id: {...}}
active_games = {}

# Language preferences: {user_id: 'hu' or 'en'}
user_languages = {}

# Egyszerű napi riasztás tároló: {user_id: {"city": str, "hour": int, "minute": int}}
user_alerts = {}

# Translations dictionary
TRANSLATIONS = {
    'weather_title': {'hu': '🌡️ Időjárás:', 'en': '🌡️ Weather:'},
    'condition': {'hu': 'Állapot', 'en': 'Condition'},
    'temperature': {'hu': 'Hőmérséklet', 'en': 'Temperature'},
    'feels_like': {'hu': 'Érzet', 'en': 'Feels like'},
    'humidity': {'hu': 'Páratartalom', 'en': 'Humidity'},
    'wind': {'hu': 'Szél', 'en': 'Wind'},
    'clothing': {'hu': '👕 Mit vegyek föl?', 'en': '👕 What to wear?'},
    'warnings': {'hu': '⚠️ Figyelmeztetések', 'en': '⚠️ Warnings'},
    'footer': {'hu': ' <:hungary:1447128233249214494> Adatok forrása: OpenWeatherMap | Figyelmeztetések: HungaroMet stílusú', 'en': ' <:hungary:1447128233249214494> Data source: OpenWeatherMap | Warnings: HungaroMet style'},
}


def get_user_lang(user_id: int) -> str:
    """Get user's preferred language, default to Hungarian."""
    return user_languages.get(user_id, 'hu')


def t(key: str, lang: str = 'hu') -> str:
    """Translate a key to the specified language."""
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get('hu', key))


def get_moon_phase(now: Optional[datetime] = None) -> str:
    """
    Egyszerű, közelítő holdfázis számítás.
    Nem csillagászati pontosságú, de Discord bothoz bőven jó.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    # Referencia: 2000-01-06 körül újhold volt (egyszerű referencia)
    known_new_moon = datetime(2000, 1, 6, tzinfo=timezone.utc)
    days = (now - known_new_moon).total_seconds() / 86400.0
    synodic_month = 29.53058867
    phase = days % synodic_month
    phase_index = int((phase / synodic_month) * 8)  # 0–7

    phases = [
        "🌑 Újhold",
        "🌒 Növő sarló",
        "🌓 Első negyed",
        "🌔 Növő hold",
        "🌕 Telihold",
        "🌖 Fogyó hold",
        "🌗 Utolsó negyed",
        "🌘 Fogyó sarló",
    ]

    return phases[phase_index % 8]


# --- BOT SETUP ---
# We need to explicitly enable message content for listening to user guesses
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# --- HELPER FUNCTIONS ---


def get_weather_data(city_name: str) -> Optional[dict]:
    """Fetches weather data from the OpenWeatherMap API."""
    params = {
        'q': city_name + ",HU",
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'hu'
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def format_weather_embed(data: dict, lang: str = 'hu') -> discord.Embed:
    if data['cod'] != 200:
        error_msg = {'hu': 'Időjárás Lekérdezési Hiba', 'en': 'Weather Query Error'}
        error_desc = {'hu': 'Nem található időjárás a megadott helyszínhez.', 'en': 'Weather data not found for the specified location.'}
        return discord.Embed(
            title=error_msg.get(lang, error_msg['hu']),
            description=error_desc.get(lang, error_desc['hu']),
            color=discord.Color.red()
        )

    city = data['name']
    weather = data['weather'][0]
    main = data['main']
    wind = data['wind']

    description = weather['description'].capitalize()
    temp = main['temp']
    feels_like = main['feels_like']

    embed = discord.Embed(
        title=f"{t('weather_title', lang)} **{city}**",
        color=discord.Color.blue()
    )

    embed.add_field(name=t('condition', lang), value=description, inline=False)
    embed.add_field(name=t('temperature', lang), value=f"**{temp:.1f}°C** ({t('feels_like', lang)}: {feels_like:.1f}°C)", inline=True)
    embed.add_field(name=t('humidity', lang), value=f"{main['humidity']}%", inline=True)
    embed.add_field(name=t('wind', lang), value=f"{wind['speed']:.1f} m/s", inline=True)

    # Clothing recommendation based on temperature
    clothing = get_clothing_recommendation(temp, weather['main'], lang)
    embed.add_field(name=t('clothing', lang), value=clothing, inline=False)

    # Weather warnings
    warnings = get_weather_warnings(temp, wind['speed'], weather['main'], main['humidity'], lang)
    if warnings:
        embed.add_field(name=t('warnings', lang), value=warnings, inline=False)

    embed.set_footer(text=t('footer', lang))

    return embed


def get_clothing_recommendation(temp: float, condition: str, lang: str = 'hu') -> str:
    """Returns clothing recommendation based on temperature and weather condition."""
    clothing = ""

    # Add gender emoji (woman more common like on Időkép.hu)
    gender_emoji = "<:woman:1447127796185829376>" if random.random() < 0.7 else "<:man:1447127794323554356>"

    clothing_text = {
        'very_cold': {'hu': f"{gender_emoji} 🧥 Vastag télikabát, sál, sapka, kesztyű - Nagyon hideg van!", 'en': f"{gender_emoji} 🧥 Heavy winter coat, scarf, hat, gloves - Very cold!"},
        'cold': {'hu': f"{gender_emoji} 🧥 Télikabát, sál és kesztyű ajánlott", 'en': f"{gender_emoji} 🧥 Winter coat, scarf and gloves recommended"},
        'chilly': {'hu': f"{gender_emoji} 🧥 Kabát, meleg pulóver és sál", 'en': f"{gender_emoji} 🧥 Coat, warm sweater and scarf"},
        'cool': {'hu': f"{gender_emoji} 🧥 Kabát vagy dzseki, pulóver", 'en': f"{gender_emoji} 🧥 Coat or jacket, sweater"},
        'mild': {'hu': f"{gender_emoji} 👔 Átmeneti dzseki, hosszú ujjú felső", 'en': f"{gender_emoji} 👔 Light jacket, long sleeves"},
        'pleasant': {'hu': f"{gender_emoji} 👕 Pulóver vagy könnyű kabát", 'en': f"{gender_emoji} 👕 Sweater or light jacket"},
        'comfortable': {'hu': f"{gender_emoji} 👕 Póló, hosszú nadrág kényelmes", 'en': f"{gender_emoji} 👕 T-shirt, long pants comfortable"},
        'warm': {'hu': f"{gender_emoji} 🩳 Póló, rövid nadrág", 'en': f"{gender_emoji} 🩳 T-shirt, shorts"},
        'hot': {'hu': f"{gender_emoji} 🩳 Könnyű ruházat, napszemüveg - Forró van!", 'en': f"{gender_emoji} 🩳 Light clothing, sunglasses - It's hot!"},
    }

    if temp < -10:
        clothing = clothing_text['very_cold'][lang]
    elif temp < 0:
        clothing = clothing_text['cold'][lang]
    elif temp < 5:
        clothing = clothing_text['chilly'][lang]
    elif temp < 10:
        clothing = clothing_text['cool'][lang]
    elif temp < 15:
        clothing = clothing_text['mild'][lang]
    elif temp < 20:
        clothing = clothing_text['pleasant'][lang]
    elif temp < 25:
        clothing = clothing_text['comfortable'][lang]
    elif temp < 30:
        clothing = clothing_text['warm'][lang]
    else:
        clothing = clothing_text['hot'][lang]

    # Add condition-specific recommendations
    extras = {
        'umbrella': {'hu': "\n🌂 Ne felejtsd el az esernyőt!", 'en': "\n🌂 Don't forget your umbrella!"},
        'waterproof': {'hu': "\n❄️ Vízálló cipő ajánlott!", 'en': "\n❄️ Waterproof shoes recommended!"},
        'sun_protection': {'hu': "\n🕶️ Naptej és sapka ajánlott!", 'en': "\n🕶️ Sunscreen and hat recommended!"},
    }

    if condition in ['Rain', 'Drizzle', 'Thunderstorm']:
        clothing += extras['umbrella'][lang]
    elif condition == 'Snow':
        clothing += extras['waterproof'][lang]
    elif temp > 25:
        clothing += extras['sun_protection'][lang]

    return clothing


def get_weather_warnings(temp: float, wind_speed: float, condition: str, humidity: int, lang: str = 'hu') -> str:
    """Returns weather warnings in HungaroMet style with emotion emojis."""
    warnings = []

    warning_texts = {
        'extreme_heat': {'hu': "😭 🔴 **HŐSÉG RIASZTÁS!** Kerüld a napot, igyál sok folyadékot!", 'en': "😭 🔴 **HEAT ALERT!** Avoid the sun, drink lots of fluids!"},
        'heat_warning': {'hu': "😱 🟠 **Hőségriadó** várható! Maradj hidratált!", 'en': "😱 🟠 **Heat Warning** expected! Stay hydrated!"},
        'hot_weather': {'hu': "😳 🟡 Meleg időjárás! Igyál sok folyadékot!", 'en': "😳 🟡 Hot weather! Drink lots of fluids!"},
        'extreme_cold': {'hu': "😭 🔵 **EXTRÉM HIDEG!** Kerüld a hosszú kinti tartózkodást!", 'en': "😭 🔵 **EXTREME COLD!** Avoid prolonged outdoor exposure!"},
        'severe_cold': {'hu': "😱 🟦 Fokozott hideg! Öltözz melegen!", 'en': "😱 🟦 Severe cold! Dress warmly!"},
        'cold_weather': {'hu': "😳 🥶 Hideg időjárás! Kabát ajánlott!", 'en': "😳 🥶 Cold weather! Coat recommended!"},
        'storm_wind': {'hu': "😭 💨 **VIHAROS SZÉL!** Vigyázz a szabadban!", 'en': "😭 💨 **STORM WINDS!** Be careful outdoors!"},
        'strong_wind': {'hu': "😱 🌬️ Erős szél várható!", 'en': "😱 🌬️ Strong winds expected!"},
        'moderate_wind': {'hu': "😳 🍃 Mérsékelten szeles időjárás", 'en': "😳 🍃 Moderately windy weather"},
        'thunderstorm': {'hu': "😭 ⛈️ **ZIVATAR FIGYELMEZTETÉS!** Keress menedéket!", 'en': "😭 ⛈️ **THUNDERSTORM WARNING!** Seek shelter!"},
        'heavy_rain': {'hu': "😱 🌧️ **Heves esőzés!** Árvízveszély lehetséges!", 'en': "😱 🌧️ **Heavy rain!** Flooding possible!"},
        'rain': {'hu': "😳 🌧️ Esős időjárás - Vigyél esernyőt!", 'en': "😳 🌧️ Rainy weather - Bring an umbrella!"},
        'freezing_rain': {'hu': "😭 🧊 **ÓNOS ESŐ VESZÉLY!** Rendkívül csúszós utak!", 'en': "😭 🧊 **FREEZING RAIN DANGER!** Extremely slippery roads!"},
        'snow': {'hu': "😳 ❄️ Havazás - Óvatosan közlekedj!", 'en': "😳 ❄️ Snow - Drive carefully!"},
        'blizzard': {'hu': "😭 🌨️ **HÓVIHAR!** Ne menj ki, ha nem muszáj!", 'en': "😭 🌨️ **BLIZZARD!** Don't go out unless necessary!"},
        'fog': {'hu': "😳 🌫️ Köd - Csökkent látási viszonyok!", 'en': "😳 🌫️ Fog - Reduced visibility!"},
        'high_humidity': {'hu': "😱 💦 Magas páratartalom - Fülledt időjárás!", 'en': "😱 💦 High humidity - Muggy weather!"},
        'low_humidity': {'hu': "😳 🏜️ Alacsony páratartalom - Igyál sok vizet!", 'en': "😳 🏜️ Low humidity - Drink lots of water!"},
        'good_weather': {'hu': "😊 ✅ Kellemes időjárás! Kiváló idő a szabadba!", 'en': "😊 ✅ Pleasant weather! Great time to go outside!"},
    }

    # Temperature warnings
    if temp > 38:
        warnings.append(warning_texts['extreme_heat'][lang])
    elif temp > 35:
        warnings.append(warning_texts['heat_warning'][lang])
    elif temp > 30:
        warnings.append(warning_texts['hot_weather'][lang])
    elif temp < -20:
        warnings.append(warning_texts['extreme_cold'][lang])
    elif temp < -10:
        warnings.append(warning_texts['severe_cold'][lang])
    elif temp < 5:
        warnings.append(warning_texts['cold_weather'][lang])

    # Wind warnings
    if wind_speed > 25:
        warnings.append(warning_texts['storm_wind'][lang])
    elif wind_speed > 17:
        warnings.append(warning_texts['strong_wind'][lang])
    elif wind_speed > 10:
        warnings.append(warning_texts['moderate_wind'][lang])

    # Precipitation and special condition warnings
    if condition == 'Thunderstorm':
        warnings.append(warning_texts['thunderstorm'][lang])
    elif condition == 'Rain':
        if temp < 0:
            warnings.append(warning_texts['freezing_rain'][lang])
        elif humidity > 85:
            warnings.append(warning_texts['heavy_rain'][lang])
        else:
            warnings.append(warning_texts['rain'][lang])
    elif condition == 'Snow':
        if wind_speed > 15:
            warnings.append(warning_texts['blizzard'][lang])
        else:
            warnings.append(warning_texts['snow'][lang])
    elif condition in ['Fog', 'Mist', 'Haze']:
        warnings.append(warning_texts['fog'][lang])

    # Humidity warnings
    if humidity > 80 and temp > 25:
        warnings.append(warning_texts['high_humidity'][lang])
    elif humidity < 30 and temp > 20:
        warnings.append(warning_texts['low_humidity'][lang])

    # Good weather notification
    if not warnings and 15 <= temp <= 25 and wind_speed < 5 and condition in ['Clear', 'Clouds']:
        warnings.append(warning_texts['good_weather'][lang])

    return "\n".join(warnings) if warnings else ""


# --- WEATHER COMMAND ---

@bot.tree.command(name="idő", description="Aktuális időjárás lekérdezése magyar városokhoz/falvakhoz.")
@app_commands.describe(helyszín="A keresett magyar város vagy falu neve (pl: 'Budapest', 'Szeged')")
async def weather_command(interaction: discord.Interaction, helyszín: str):
    await interaction.response.defer()

    lang = get_user_lang(interaction.user.id)
    weather_data = get_weather_data(helyszín)

    if weather_data and weather_data.get('cod') == 200:
        embed = format_weather_embed(weather_data, lang)
        await interaction.followup.send(embed=embed)
    else:
        error_msg = "⚠️ Nem találtam időjárási adatot a(z) **{helyszín}** helyszínhez. Ellenőrizd a helyesírást!" if lang == 'hu' else f"⚠️ No weather data found for **{helyszín}**. Check the spelling!"
        await interaction.followup.send(error_msg, ephemeral=True)


# --- NEW: MULTI-CITY WEATHER ---

@bot.tree.command(
    name="tobbvaros",
    description="Több magyar város időjárásának egyidejű lekérdezése (max. 5 város)."
)
@app_commands.describe(
    varosok="Városok vesszővel elválasztva (pl.: Budapest, Szeged, Debrecen)"
)
async def multi_city_weather(interaction: discord.Interaction, varosok: str):
    await interaction.response.defer()
    lang = get_user_lang(interaction.user.id)

    city_names = [v.strip() for v in varosok.split(",") if v.strip()]
    city_names = city_names[:5]

    if not city_names:
        msg = "Adj meg legalább egy várost!" if lang == "hu" else "Please provide at least one city!"
        await interaction.followup.send(msg, ephemeral=True)
        return

    embed = discord.Embed(
        title="📊 Több város időjárása" if lang == "hu" else "📊 Multi-city Weather",
        color=discord.Color.blurple()
    )

    any_ok = False
    for name in city_names:
        data = get_weather_data(name)
        if not data or data.get("cod") != 200:
            field_value = (
                f"⚠️ Nem találtam adatot a(z) **{name}** városhoz."
                if lang == "hu"
                else f"⚠️ No weather data for **{name}**."
            )
            embed.add_field(name=name, value=field_value, inline=False)
            continue

        any_ok = True
        main = data["main"]
        weather = data["weather"][0]
        desc = weather["description"].capitalize()
        temp = main["temp"]
        hum = main["humidity"]

        value = (
            f"🌡️ **{temp:.1f}°C**\n"
            f"💧 {hum}%\n"
            f"☁️ {desc}"
        )
        embed.add_field(name=data["name"], value=value, inline=True)

    if not any_ok:
        msg = "Egyik városhoz sem sikerült adatot lekérni." if lang == "hu" else "Failed to fetch data for all cities."
        await interaction.followup.send(msg, ephemeral=True)
        return

    embed.set_footer(text=t("footer", lang))
    await interaction.followup.send(embed=embed)


# --- NEW: ASTRONOMICAL + SUNRISE/SUNSET ---

@bot.tree.command(
    name="csillagasz",
    description="Csillagászati és napkelte/napnyugta adatok magyar városokhoz."
)
@app_commands.describe(
    helyszin="Magyar város vagy falu neve (pl.: Budapest)"
)
async def astronomy_command(interaction: discord.Interaction, helyszin: str):
    await interaction.response.defer()
    lang = get_user_lang(interaction.user.id)

    data = get_weather_data(helyszin)
    if not data or data.get("cod") != 200:
        msg = (
            f"⚠️ Nem találtam adatot a(z) **{helyszin}** helyszínhez."
            if lang == "hu"
            else f"⚠️ No data found for **{helyszin}**."
        )
        await interaction.followup.send(msg, ephemeral=True)
        return

    city = data["name"]
    sys_data = data.get("sys", {})
    sunrise_ts = sys_data.get("sunrise")
    sunset_ts = sys_data.get("sunset")

    if sunrise_ts is None or sunset_ts is None:
        msg = "Nem érhetők el napkelte/napnyugta adatok." if lang == "hu" else "Sunrise/Sunset data not available."
        await interaction.followup.send(msg, ephemeral=True)
        return

    sunrise = datetime.fromtimestamp(sunrise_ts, tz=timezone.utc).astimezone()
    sunset = datetime.fromtimestamp(sunset_ts, tz=timezone.utc).astimezone()

    moon_phase_text = get_moon_phase()

    if lang == "hu":
        title = f"🌌 Csillagászati adatok - {city}"
        sunrise_str = sunrise.strftime("%H:%M")
        sunset_str = sunset.strftime("%H:%M")
        desc = (
            f"🌅 **Napkelte:** {sunrise_str}\n"
            f"🌇 **Napnyugta:** {sunset_str}\n"
            f"🌙 **Hold fázisa:** {moon_phase_text}\n"
        )
    else:
        title = f"🌌 Astronomical data - {city}"
        sunrise_str = sunrise.strftime("%H:%M")
        sunset_str = sunset.strftime("%H:%M")
        phase_map = {
            "Újhold": "New Moon",
            "Növő sarló": "Waxing Crescent",
            "Első negyed": "First Quarter",
            "Növő hold": "Waxing Gibbous",
            "Telihold": "Full Moon",
            "Fogyó hold": "Waning Gibbous",
            "Utolsó negyed": "Last Quarter",
            "Fogyó sarló": "Waning Crescent",
        }
        # csak a magyar részre próbál rá
        phase_en = moon_phase_text
        for hu_name, en_name in phase_map.items():
            if hu_name in moon_phase_text:
                phase_en = en_name
                break

        desc = (
            f"🌅 **Sunrise:** {sunrise_str}\n"
            f"🌇 **Sunset:** {sunset_str}\n"
            f"🌙 **Moon phase:** {phase_en}\n"
        )

    embed = discord.Embed(
        title=title,
        description=desc,
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text=t("footer", lang))
    await interaction.followup.send(embed=embed)


# --- NEW: SIMPLE DAILY ALERT PERSISTENCE (IN-MEMORY) ---

@bot.tree.command(
    name="riasztas",
    description="Napi időjárás-riasztás beállítása egy városhoz."
)
@app_commands.describe(
    helyszin="Magyar város neve (pl.: Budapest)",
    ora="Óra (0–23)",
    perc="Perc (0–59)"
)
async def set_alert(interaction: discord.Interaction, helyszin: str, ora: int, perc: int):
    lang = get_user_lang(interaction.user.id)

    if not (0 <= ora <= 23 and 0 <= perc <= 59):
        msg = "⚠️ Érvénytelen időpont (óra: 0-23, perc: 0-59)." if lang == "hu" else "⚠️ Invalid time (hour: 0–23, minute: 0–59)."
        await interaction.response.send_message(msg, ephemeral=True)
        return

    data = get_weather_data(helyszin)
    if not data or data.get("cod") != 200:
        msg = (
            f"⚠️ Nem találtam adatot a(z) **{helyszin}** helyszínhez."
            if lang == "hu"
            else f"⚠️ No data found for **{helyszin}**."
        )
        await interaction.response.send_message(msg, ephemeral=True)
        return

    user_alerts[interaction.user.id] = {
        "city": data["name"],
        "hour": ora,
        "minute": perc,
    }

    if lang == "hu":
        msg = f"✅ Riasztás beállítva: **{data['name']}**, minden nap **{ora:02d}:{perc:02d}**-kor."
    else:
        msg = f"✅ Alert set for **{data['name']}**, every day at **{ora:02d}:{perc:02d}**."
    await interaction.response.send_message(msg, ephemeral=True)


@bot.tree.command(
    name="riasztastorol",
    description="Korábban beállított napi riasztás törlése."
)
async def clear_alert(interaction: discord.Interaction):
    lang = get_user_lang(interaction.user.id)

    if interaction.user.id not in user_alerts:
        msg = "Nincs aktív riasztásod." if lang == "hu" else "You have no active alerts."
        await interaction.response.send_message(msg, ephemeral=True)
        return

    del user_alerts[interaction.user.id]
    msg = "✅ Riasztás törölve." if lang == "hu" else "✅ Alert cleared."
    await interaction.response.send_message(msg, ephemeral=True)


# --- SLASH COMMAND: LANGUAGE ---

@bot.tree.command(name="nyelv", description="Váltsd meg a bot nyelvét / Change bot language")
@app_commands.describe(language="Choose language: hu (Magyar) or en (English)")
@app_commands.choices(language=[
    app_commands.Choice(name="🇭🇺 Magyar", value="hu"),
    app_commands.Choice(name="🇬🇧 English", value="en")
])
async def set_language(interaction: discord.Interaction, language: str):
    """Set user's preferred language."""
    user_languages[interaction.user.id] = language

    if language == 'hu':
        msg = "✅ Nyelv beállítva: **Magyar** 🇭🇺"
    else:
        msg = "✅ Language set to: **English** 🇬🇧"

    await interaction.response.send_message(msg, ephemeral=True)


# --- SLASH COMMAND: HELP ---

@bot.tree.command(name="help", description="Segítség és parancsok listája")
async def help_slash_command(interaction: discord.Interaction):
    """Segítség és parancsok listája."""
    embed = discord.Embed(
        title="🌤️ Időjáró Bot - Parancsok",
        description="Az Időjáró Bot segít időjárási adatokat lekérdezni és szórakoztató játékokat játszani!",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📊 Időjárás Lekérdezés",
        value="`/idő <helyszín>` - Időjárás lekérdezése\nPélda: `/idő Budapest`",
        inline=False
    )

    embed.add_field(
        name="🎮 Játékok",
        value=(
            "`/tippelj` - Találd ki a várost az időjárás alapján!\n"
            "`/osszehasomlit <város1> <város2>` - Hasonlítsd össze két város időjárását\n"
            "`/vetélkedő` - Indíts időjárás vetélkedőt több játékossal"
        ),
        inline=False
    )

    embed.add_field(
        name="🌡️ Statisztikák",
        value=(
            "`/legmelegebb` - Melyik magyar város a legmelegebb most?\n"
            "`/leghidegebb` - Melyik magyar város a leghidegebb most?\n"
            "`/terkep` - Időjárási térkép linkek"
        ),
        inline=False
    )

    embed.add_field(
        name="👔 Öltözködés",
        value="`/mitvegyekfol <helyszín>` - Öltözködési tanácsok az időjárás alapján",
        inline=False
    )

    embed.add_field(
        name="🌌 Csillagászat & riasztás",
        value=(
            "`/csillagasz <helyszin>` - Napkelte, napnyugta, Hold fázis\n"
            "`/tobbvaros <lista>` - Több város időjárása egyszerre\n"
            "`/riasztas <helyszin> <óra> <perc>` - Napi időjárás-riasztás beállítása\n"
            "`/riasztastorol` - Riasztás törlése"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Egyéb",
        value=(
            "`/info` - Bot információk\n"
            "`/ping` - Bot válaszidő\n"
            "`/vicc` - Időjárással kapcsolatos vicc"
        ),
        inline=False
    )

    embed.set_footer(text="Adatok forrása: OpenWeatherMap")
    await interaction.response.send_message(embed=embed)


# --- SLASH COMMAND: MIT VEGYEK FÖL ---

@bot.tree.command(name="mitvegyekfol", description="Mit vegyek föl ma? Öltözködési tanácsok az időjárás alapján")
@app_commands.describe(helyszín="A keresett magyar város vagy falu neve")
async def clothing_advice(interaction: discord.Interaction, helyszín: str):
    """Öltözködési tanácsok az időjárás alapján."""
    await interaction.response.defer()

    weather_data = get_weather_data(helyszín)

    if not weather_data or weather_data.get('cod') != 200:
        await interaction.followup.send(f"⚠️ Nem találtam időjárási adatot a(z) **{helyszín}** helyszínhez.", ephemeral=True)
        return

    city = weather_data['name']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    condition = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description'].capitalize()

    clothing = get_clothing_recommendation(temp, condition)

    embed = discord.Embed(
        title=f"👔 Mit vegyek föl? - {city}",
        description=f"**{temp:.1f}°C** (Érzet: {feels_like:.1f}°C)\n{description}",
        color=discord.Color.purple()
    )

    embed.add_field(name="Öltözködési tanács", value=clothing, inline=False)

    tips = []
    if temp < 0:
        tips.append("🧊 Réteges öltözködés ajánlott!")
    if condition in ['Rain', 'Drizzle', 'Thunderstorm']:
        tips.append("☔ Vízálló ruházat!")
    if temp > 28:
        tips.append("💧 Lélegző, könnyű anyagok!")

    if tips:
        embed.add_field(name="💡 Extra tippek", value="\n".join(tips), inline=False)

    embed.set_footer(text=f"Időjárás: {city}")

    await interaction.followup.send(embed=embed)


# --- SLASH COMMAND: INFO ---

@bot.tree.command(name="info", description="Bot információk")
async def info_slash_command(interaction: discord.Interaction):
    """Bot információk."""
    embed = discord.Embed(
        title="🌤️ Időjáró Bot",
        description="Magyar időjárási adatokat szolgáltató Discord bot",
        color=discord.Color.green()
    )

    embed.add_field(name="Verzió", value="1.1.1", inline=True)
    embed.add_field(name="Szerverek", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="API", value="OpenWeatherMap", inline=True)
    embed.add_field(name="Városok", value=str(len(HUNGARIAN_CITIES)), inline=True)
    embed.add_field(name="Python", value="discord.py", inline=True)
    embed.add_field(name="Nyelv", value="Magyar 🇭🇺", inline=True)
    embed.add_field(name="Github repó", value="https://github.com/urbanmove8-qatar/idojarobot", inline=True)

    embed.set_footer(text="Köszönjük, hogy használod az Időjáró Botot!")
    await interaction.response.send_message(embed=embed)


# --- SLASH COMMAND: PING ---

@bot.tree.command(name="ping", description="Bot válaszidő ellenőrzése")
async def ping_slash_command(interaction: discord.Interaction):
    """Bot válaszidő ellenőrzése."""
    latency = round(bot.latency * 1000)

    if latency < 100:
        emoji = "🟢"
        status = "Kiváló"
    elif latency < 200:
        emoji = "🟡"
        status = "Jó"
    else:
        emoji = "🔴"
        status = "Lassú"

    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"{emoji} Bot válaszidő: **{latency}ms** ({status})",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)


# --- SLASH COMMAND: ÖSSZEHASONLÍT ---

@bot.tree.command(name="osszehasonlit", description="Hasonlítsd össze két város időjárását")
@app_commands.describe(
    város1="Első város neve",
    város2="Második város neve"
)
async def compare_weather(interaction: discord.Interaction, város1: str, város2: str):
    """Két város időjárásának összehasonlítása."""
    await interaction.response.defer()

    weather1 = get_weather_data(város1)
    weather2 = get_weather_data(város2)

    if not weather1 or weather1.get('cod') != 200:
        await interaction.followup.send(f"⚠️ Nem találtam időjárási adatot a(z) **{város1}** helyszínhez.", ephemeral=True)
        return

    if not weather2 or weather2.get('cod') != 200:
        await interaction.followup.send(f"⚠️ Nem találtam időjárási adatot a(z) **{város2}** helyszínhez.", ephemeral=True)
        return

    city1 = weather1['name']
    city2 = weather2['name']
    temp1 = weather1['main']['temp']
    temp2 = weather2['main']['temp']
    desc1 = weather1['weather'][0]['description'].capitalize()
    desc2 = weather2['weather'][0]['description'].capitalize()

    temp_diff = abs(temp1 - temp2)
    warmer_city = city1 if temp1 > temp2 else city2

    embed = discord.Embed(
        title=f"⚖️ {city1} vs {city2}",
        description=f"Hőmérséklet különbség: **{temp_diff:.1f}°C**",
        color=discord.Color.purple()
    )

    embed.add_field(
        name=f"🏙️ {city1}",
        value=f"**{temp1:.1f}°C**\n{desc1}\nPáratartalom: {weather1['main']['humidity']}%",
        inline=True
    )

    embed.add_field(
        name=f"🏙️ {city2}",
        value=f"**{temp2:.1f}°C**\n{desc2}\nPáratartalom: {weather2['main']['humidity']}%",
        inline=True
    )

    if temp_diff > 5:
        embed.set_footer(text=f"🔥 {warmer_city} jelentősen melegebb!")
    elif temp_diff > 2:
        embed.set_footer(text=f"☀️ {warmer_city} egy kicsit melegebb")
    else:
        embed.set_footer(text="🤝 Hasonló hőmérséklet mindkét városban!")

    await interaction.followup.send(embed=embed)


# --- SLASH COMMAND: LEGMELEGEBB ---

@bot.tree.command(name="legmelegebb", description="Melyik magyar város a legmelegebb most?")
async def hottest_city(interaction: discord.Interaction):
    """Megkeresi a legmelegebb magyar várost."""
    await interaction.response.defer()

    max_temp = -999
    hottest = None
    hottest_data = None

    sample_cities = random.sample(HUNGARIAN_CITIES, min(15, len(HUNGARIAN_CITIES)))

    for city in sample_cities:
        data = get_weather_data(city)
        if data and data.get('cod') == 200:
            temp = data['main']['temp']
            if temp > max_temp:
                max_temp = temp
                hottest = city
                hottest_data = data

    if hottest_data:
        embed = discord.Embed(
            title=f"🔥 Legmelegebb város: {hottest_data['name']}",
            description=f"**{max_temp:.1f}°C**",
            color=discord.Color.red()
        )
        embed.add_field(name="Időjárás", value=hottest_data['weather'][0]['description'].capitalize(), inline=True)
        embed.add_field(name="Páratartalom", value=f"{hottest_data['main']['humidity']}%", inline=True)
        embed.set_footer(text=f"Mintavétel: {len(sample_cities)} város")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Sajnos nem sikerült adatokat gyűjteni.", ephemeral=True)


# --- SLASH COMMAND: LEGHIDEGEBB ---

@bot.tree.command(name="leghidegebb", description="Melyik magyar város a leghidegebb most?")
async def coldest_city(interaction: discord.Interaction):
    """Megkeresi a leghidegebb magyar várost."""
    await interaction.response.defer()

    min_temp = 999
    coldest = None
    coldest_data = None

    sample_cities = random.sample(HUNGARIAN_CITIES, min(15, len(HUNGARIAN_CITIES)))

    for city in sample_cities:
        data = get_weather_data(city)
        if data and data.get('cod') == 200:
            temp = data['main']['temp']
            if temp < min_temp:
                min_temp = temp
                coldest = city
                coldest_data = data

    if coldest_data:
        embed = discord.Embed(
            title=f"❄️ Leghidegebb város: {coldest_data['name']}",
            description=f"**{min_temp:.1f}°C**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Időjárás", value=coldest_data['weather'][0]['description'].capitalize(), inline=True)
        embed.add_field(name="Páratartalom", value=f"{coldest_data['main']['humidity']}%", inline=True)
        embed.set_footer(text=f"Mintavétel: {len(sample_cities)} város")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Sajnos nem sikerült adatokat gyűjteni.", ephemeral=True)


# --- SLASH COMMAND: TÉRKÉP ---

@bot.tree.command(name="terkep", description="Időjárási térkép linkek")
async def weather_map(interaction: discord.Interaction):
    """Időjárási térkép linkek."""
    embed = discord.Embed(
        title="🗺️ Időjárási Térképek",
        description="Hasznos online időjárási térképek Magyarországhoz",
        color=discord.Color.teal()
    )

    embed.add_field(
        name="🌍 OpenWeatherMap",
        value="[Interaktív térkép](https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat=47.1625&lon=19.5033&zoom=7)",
        inline=False
    )

    embed.add_field(
        name="🇭🇺 Met.hu",
        value="[Magyar Meteorológiai Szolgálat](https://www.met.hu)",
        inline=False
    )

    embed.add_field(
        name="🇭🇺 Időkép.hu",
        value="[Időkép.hu](https://www.idokep.hu)",
        inline=False
    )

    embed.add_field(
        name="🌧️ Windy",
        value="[Windy.com Magyarország](https://www.windy.com/?47.162,19.503,7)",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


# --- SLASH COMMAND: VICC ---

@bot.tree.command(name="vicc", description="Időjárással kapcsolatos vicc")
async def weather_joke(interaction: discord.Interaction):
    """Random időjárási vicc."""
    jokes = [
        "Miért nem mennek a programozók ki esőben? Mert attól félnek, hogy lemossa őket a felhő! ☁️",
        "Mit mond az időjós, ha találkozik egy másik időjóssal? - Szép idő, nem? 🌞",
        "Miért szeretik a magyarok a felhőket? Mert ingyen vannak! ☁️💰",
        "Mi a különbség az időjárás-jelentés és egy vicc között? A vicc néha vicces. 😅",
        "Milyen az ideális időjárás? Amikor az előrejelzés megegyezik a valósággal! 🎯",
        "Miért hord az esernyő szemüveget? Mert esős! 🌧️👓",
        "Mi a napfény kedvenc zenéje? A fényes dallamok! ☀️🎵",
        "Miért nem tud a szél állást kapni? Mert mindig elfújja az interjút! 💨😂",
        "Hogy hívják a hűvös időben sétáló informatikust? Letöltött fájl. ❄️",
        "Mit csinál a programozó a viharban? Megpróbálja 'debugolni' a villámokat. ⚡",
        "Miért nem félnek a felhők a kudarctól? Mert mindig van 'backup' az égen. ☁️☁️",
        "Hogy hívják a hóembert nyáron? Tócsi. ☃️💧",
        "Miért nem veszekszik a Nap a Holddal? Mert nincs köztük légkör. ☀️🌙",
        "Mit mond a kis felhő az anyukájának? 'Mama, ha nagy leszek, én is tornádó akarok lenni!' 🌪️",
        "Hogy hívják a félénk villámot? Csendes-óceáni. ⛈️",
        "Melyik a szél kedvenc tantárgya? A fúvós hangszerek. 🎷💨",
        "Hogy hívják a sivatagi esőt? Délibáb-szerviz. 🌵☔",
        "Mit csinál a felhő, ha viszket a háta? Keres egy felhőkarcolót! 🏙️☁️",
        "Miért nem lehet a széllel kártyázni? Mert mindig megkavarja a lapokat! 🃏",
        "Mi az: zöld és esik az égből? Egy hősugárzó, csak rossz a színe. 🍏🌧️",
        "Hogy nevezik a nagyon lassú vihart? Vánszorgó-vihar. 🐌⚡",
        "Miért visz a programozó esernyőt a szerverszobába? Mert ott is van Cloud! 💻☁️",
        "Mit mond a jégeső a tetőnek? 'Bocs, csak beugrottam!' 🏠❄️",
        "Mi a villám kedvenc étele? A sült-krumpli, de csak ha jól meg van sütve. 🍟⚡",
        "Hogy hívják a brit napsütést? Véletlen. 🇬🇧☀️",
        "Mit csinál a Nap, ha elfárad? Lemegy pihenni. 🌅",
        "Miért hord a szél kalapot? Hogy ne legyen olyan 'széltolt'. 🎩💨",
        "Hogy hívják a digitális esőt? Adatfolyam. 💾🌧️"
    ]

    joke = random.choice(jokes)

    embed = discord.Embed(
        title="<:laughing:1447128231701381323> Időjárás Vicc",
        description=joke,
        color=discord.Color.gold()
    )

    await interaction.response.send_message(embed=embed)


# --- PREFIX COMMAND: IDŐ ---

@bot.command(name='idő', aliases=['ido', 'weather'])
async def weather_prefix_command(ctx, *, helyszín: str):
    """Aktuális időjárás lekérdezése magyar városokhoz/falvakhoz."""
    async with ctx.typing():
        weather_data = get_weather_data(helyszín)

        if weather_data and weather_data.get('cod') == 200:
            embed = format_weather_embed(weather_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"⚠️ Nem találtam időjárási adatot a(z) **{helyszín}** helyszínhez. Ellenőrizd a helyesírást!")


# --- PREFIX COMMAND: HELP ---

@bot.command(name='help', aliases=['segitseg', 'segítség'])
async def help_command(ctx):
    """Segítség és parancsok listája."""
    embed = discord.Embed(
        title="🌤️ Időjáró Bot - Parancsok",
        description="Az Időjáró Bot segít időjárási adatokat lekérdezni és játékokat játszani!",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📊 Időjárás Lekérdezés",
        value=(
            "**Slash parancs:** `/idő <helyszín>`\n"
            "**Prefix parancs:** `idojaras!idő <helyszín>` vagy `idojaras!ido <helyszín>`\n"
            "Példa: `idojaras!idő Budapest`"
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 Tippelő Játék",
        value=(
            "**Slash parancs:** `/tippelj`\n"
            "**Prefix parancs:** `idojaras!tippelj`\n"
            "Indíts egy játékot, ahol ki kell találnod a várost az időjárási adatok alapján!"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Egyéb Parancsok",
        value=(
            "`idojaras!help` - Ez a segítség menü\n"
            "`idojaras!info` - Bot információk\n"
            "`idojaras!ping` - Bot válaszidő ellenőrzése"
        ),
        inline=False
    )

    embed.set_footer(text="Adatok forrása: OpenWeatherMap")
    await ctx.send(embed=embed)


# --- PREFIX COMMAND: INFO ---

@bot.command(name='info', aliases=['about'])
async def info_command(ctx):
    """Bot információk."""
    embed = discord.Embed(
        title="🌤️ Időjáró Bot",
        description="Magyar időjárási adatokat szolgáltató Discord bot",
        color=discord.Color.green()
    )

    embed.add_field(name="Verzió", value="1.1.0", inline=True)
    embed.add_field(name="Szerver szám", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Prefix", value="`idojaras!`", inline=True)
    embed.add_field(name="API", value="OpenWeatherMap", inline=True)
    embed.add_field(name="Python", value="discord.py", inline=True)
    embed.add_field(name="Nyelv", value="Magyar 🇭🇺", inline=True)

    embed.set_footer(text="Köszönjük, hogy használod az Időjáró Botot!")
    await ctx.send(embed=embed)


# --- PREFIX COMMAND: PING ---

@bot.command(name='ping')
async def ping_command(ctx):
    """Bot válaszidő ellenőrzése."""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot válaszidő: **{latency}ms**",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)


# --- WEATHER GAME COMMAND (SLASH) ---

@bot.tree.command(name="tippelj", description="Indíts egy 'Melyik Város Ez?' időjárás tippelő játékot.")
@app_commands.describe(nehézség="Válassz nehézségi szintet / Choose difficulty")
@app_commands.choices(nehézség=[
    app_commands.Choice(name="🟢 Könnyű / Easy", value="easy"),
    app_commands.Choice(name="🟡 Közepes / Medium", value="medium"),
    app_commands.Choice(name="🔴 Nehéz / Hard", value="hard")
])
async def start_game(interaction: discord.Interaction, nehézség: str = "medium"):
    """
    Starts the Weather Guessing Game in the current channel with difficulty levels.
    """
    channel_id = interaction.channel_id
    lang = get_user_lang(interaction.user.id)

    if channel_id in active_games:
        msg = f"Egy játék már fut ebben a csatornában! Próbálj tippelni: **{active_games[channel_id]['city']}**" if lang == 'hu' else f"A game is already running in this channel! Try guessing: **{active_games[channel_id]['city']}**"
        await interaction.response.send_message(msg, ephemeral=True)
        return

    correct_city = random.choice(HUNGARIAN_CITIES)
    weather_data = get_weather_data(correct_city)

    if not weather_data or weather_data.get('cod') != 200:
        error_msg = "Sajnálom, hiba történt az időjárási adatok lekérésekor. Próbáld újra később." if lang == 'hu' else "Sorry, an error occurred while fetching weather data. Try again later."
        await interaction.response.send_message(error_msg, ephemeral=True)
        return

    weather = weather_data['weather'][0]
    main = weather_data['main']

    description = weather['description'].capitalize()
    temp_min = main['temp_min']
    temp_max = main['temp_max']
    temp_avg = (temp_min + temp_max) / 2

    active_games[channel_id] = {
        'city': correct_city.lower(),
        'difficulty': nehézség,
        'hints_used': 0,
        'weather_data': weather_data
    }

    title = "❓ Melyik Magyar Város Ez? ❓" if lang == 'hu' else "❓ Which Hungarian City Is This? ❓"
    desc = "A feladatod kitalálni, melyik város időjárását látod!" if lang == 'hu' else "Your task is to guess which city's weather you see!"

    game_embed = discord.Embed(
        title=title,
        description=desc,
        color=discord.Color.gold()
    )

    if nehézség == "easy":
        game_embed.add_field(name="🌡️ Hőmérséklet / Temperature", value=f"**{temp_avg:.1f}°C**", inline=True)
        game_embed.add_field(name="☁️ Időjárási Állapot / Condition", value=f"**{description}**", inline=True)
        game_embed.add_field(name="💧 Páratartalom / Humidity", value=f"{main['humidity']}%", inline=True)
        first_letter = correct_city[0].upper()
        game_embed.add_field(name="💡 Hint", value=f"Kezdőbetű / First letter: **{first_letter}**", inline=False)
    elif nehézség == "medium":
        game_embed.add_field(name="🌡️ Hőmérséklet Tartomány / Temp Range", value=f"**{temp_min:.1f}°C** - **{temp_max:.1f}°C**", inline=True)
        game_embed.add_field(name="☁️ Időjárás / Weather", value=f"**{description}**", inline=True)
    else:
        game_embed.add_field(name="🌡️ Hőmérséklet / Temperature", value=f"**~{int(temp_avg/5)*5}°C körül / around**", inline=True)
        game_embed.add_field(name="💧 Páratartalom / Humidity", value=f"~{int(main['humidity']/10)*10}%", inline=True)

    footer_text = "Tippelj egy városnévvel! Pl: Szeged | Használd: /hint" if lang == 'hu' else "Guess with a city name! E.g.: Szeged | Use: /hint"
    game_embed.set_footer(text=footer_text)

    await interaction.response.send_message(embed=game_embed)


# --- SLASH COMMAND: HINT ---

@bot.tree.command(name="hint", description="Kérj segítséget a tippelő játékhoz / Get a hint for the guessing game")
async def give_hint(interaction: discord.Interaction):
    """Provide hints for the active guessing game."""
    channel_id = interaction.channel_id
    lang = get_user_lang(interaction.user.id)

    if channel_id not in active_games:
        msg = "Nincs aktív játék ebben a csatornában! Indíts egyet a `/tippelj` paranccsal!" if lang == 'hu' else "No active game in this channel! Start one with `/tippelj`!"
        await interaction.response.send_message(msg, ephemeral=True)
        return

    game = active_games[channel_id]
    game['hints_used'] += 1
    city = game['city']

    hints = []

    if game['hints_used'] == 1:
        hint_text = f"💡 A város neve **{len(city)} betű** hosszú!" if lang == 'hu' else f"💡 The city name is **{len(city)} letters** long!"
        hints.append(hint_text)
    elif game['hints_used'] == 2:
        hint_text = f"💡 Kezdőbetű: **{city[0].upper()}**, Utolsó betű: **{city[-1].upper()}**" if lang == 'hu' else f"💡 First letter: **{city[0].upper()}**, Last letter: **{city[-1].upper()}**"
        hints.append(hint_text)
    elif game['hints_used'] == 3:
        regions = {
            'budapest': 'Főváros / Capital',
            'debrecen': 'Kelet-Magyarország / Eastern Hungary',
            'szeged': 'Dél-Magyarország / Southern Hungary',
            'miskolc': 'Északkelet-Magyarország / Northeastern Hungary',
            'pecs': 'Délnyugat-Magyarország / Southwestern Hungary',
        }
        region = regions.get(city, 'Magyarország / Hungary')
        hint_text = f"💡 Régió / Region: **{region}**"
        hints.append(hint_text)
    else:
        visible = city[:len(city)//2]
        hidden = '_' * (len(city) - len(visible))
        hint_text = f"💡 **{visible.upper()}{hidden}**"
        hints.append(hint_text)

    await interaction.response.send_message('\n'.join(hints), ephemeral=False)


# --- SLASH COMMAND: FELADÁS ---

@bot.tree.command(name="feladas", description="Add fel a játékot / Give up the game")
async def give_up(interaction: discord.Interaction):
    """Give up the current game."""
    channel_id = interaction.channel_id
    lang = get_user_lang(interaction.user.id)

    if channel_id not in active_games:
        msg = "Nincs aktív játék ebben a csatornában!" if lang == 'hu' else "No active game in this channel!"
        await interaction.response.send_message(msg, ephemeral=True)
        return

    correct_city = active_games[channel_id]['city']
    del active_games[channel_id]

    msg = f"😔 A helyes válasz: **{correct_city.capitalize()}** volt!" if lang == 'hu' else f"😔 The correct answer was: **{correct_city.capitalize()}**!"
    await interaction.response.send_message(msg)

def normalize_city_name(name: str) -> str:
    """Normalize city name: lowercase, remove accents, clean spaces"""
    name = name.strip().lower()
    # Remove accents
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    # Clean multiple spaces
    name = ' '.join(name.split())
    return name

# --- PREFIX COMMAND: TIPPELJ ---

@bot.command(name='tippelj', aliases=['jatek', 'játék', 'game'])
async def tippelj_prefix_command(ctx):
    """Indíts egy 'Melyik Város Ez?' időjárás tippelő játékot."""
    channel_id = ctx.channel.id

    if channel_id in active_games:
        display_city = active_games[channel_id].get('display_city', active_games[channel_id]['city'].capitalize())
        await ctx.send(f"🎮 Egy játék már fut ebben a csatornában! A helyes válasz: **{display_city}**")
        return

    correct_city = random.choice(HUNGARIAN_CITIES)
    weather_data = get_weather_data(correct_city)

    if not weather_data or weather_data.get('cod') != 200:
        await ctx.send("❌ Sajnálom, hiba történt az időjárási adatok lekérésekor. Próbáld újra később.")
        return

    weather = weather_data['weather'][0]
    main = weather_data['main']

    description = weather['description'].capitalize()
    temp_min = main['temp_min']
    temp_max = main['temp_max']

    # JAVÍTOTT: Normalizált név tárolása + eredeti megjelenítés
    normalized_city = normalize_city_name(correct_city)
    
    active_games[channel_id] = {
        'city': normalized_city,  # Ékezet nélküli, kisbetűs verzió
        'display_city': correct_city,  # Eredeti forma a kiíráshoz
        'difficulty': 'prefix',
        'hints_used': 0,
        'weather_data': weather_data
    }

    game_embed = discord.Embed(
        title="❓ Melyik Magyar Város Ez? ❓",
        description="A feladatod kitalálni, melyik város időjárását látod!",
        color=discord.Color.gold()
    )

    game_embed.add_field(name="🌤️ Időjárási Állapot", value=f"**{description}**", inline=False)
    game_embed.add_field(name="🌡️ Hőmérséklet Tartomány", value=f"**{temp_min:.1f}°C** és **{temp_max:.1f}°C** között", inline=True)
    game_embed.add_field(name="💧 Páratartalom", value=f"{main['humidity']}%", inline=True)
    game_embed.set_footer(text="💡 Tippelj egy városnévvel! Pl: pecs, szeged, budapest")

    await ctx.send(embed=game_embed)


# --- MESSAGE LISTENER FOR GUESSING ---

@bot.event
async def on_message(message: discord.Message):
    """
    Listens for user messages to check for guesses if a game is active.
    """
    if message.author.bot:
        return

    channel_id = message.channel.id
    user_guess_raw = message.content.strip()
    user_guess_normalized = normalize_city_name(user_guess_raw)

    if channel_id in active_games and len(user_guess_raw) > 1:
        game_data = active_games[channel_id]
        correct_normalized = game_data['city']
        
        # JAVÍTOTT: Biztonságos .get() használata
        display_city = game_data.get('display_city', correct_normalized.capitalize())

        # 🎯 PONTOS TALÁLAT
        if user_guess_normalized == correct_normalized:
            await message.channel.send(
                f"🎉 **Gratulálok, {message.author.mention}!** "
                f"Kitaláltad! A helyes város **{display_city}** volt! ⛅"
            )
            del active_games[channel_id]
            return

        # 🤔 RÉSZLEGES TALÁLAT (reakció)
        elif len(user_guess_normalized) > 2:
            if (user_guess_normalized in correct_normalized or 
                correct_normalized in user_guess_normalized):
                await message.add_reaction("🤔")

    await bot.process_commands(message)

# --- BOT EVENTS ---

@bot.event
async def on_ready():
    print(f'Időjáró bejelentkezve: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Szerverek száma: {len(bot.guilds)}')
    print(f'Slash parancsok aktívak!')
    print('-' * 40)
    try:
        synced = await bot.tree.sync()
        print(f"✅ Szinkronizálva {len(synced)} slash parancs.")
    except Exception as e:
        print(f"❌ Hiba a parancs szinkronizálásakor: {e}")


# --- BOT RUN ---
if __name__ == "__main__":
    if not DISCORD_TOKEN or not WEATHER_API_KEY:
        print("HIBA: A konfigurációs kulcsok hiányoznak a kódból!")
    else:
        bot.run(DISCORD_TOKEN)
