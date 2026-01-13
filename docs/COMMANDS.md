# Parancsok (Commands)

Ez a fájl részletesen dokumentálja az Időjáróbot parancsait — mind a slash (újabb Discord API), mind a prefix (klasszikus) parancsok példáival, paramétereivel és viselkedésével.

Általános jelölés
- /parancs — slash (gondoskodik az autocomplete-ről és paraméterek ellenőrzéséről)
- !parancs — prefix parancs (régebbi botoknál gyakori)
- [opcionális] — opcionális paraméter
- <kötelező> — kötelező paraméter

----------------------------------------
Tartalomjegyzék
1. Alap parancsok
2. Időjárás lekérdezés
3. Öltözködési tanácsok
4. Játékok
5. Segítség és információ
6. Hibakezelés és visszajelzés
7. Parancs kiterjesztés — sablon fejlesztőknek

----------------------------------------
1. Alap parancsok

- /ping
  - Leírás: Gyors válaszüzenet — a bot késleltetésének mérése.
  - Példa: `/ping`
  - Válasz: "Pong! Latency: 123ms"

- /info
  - Leírás: Bot verzió, támogatott városok száma, források.
  - Példa: `/info`

- /help
  - Leírás: Részletes segítség a parancsokról (ez a parancs jelen dokumentum rövidített változatát adhatja vissza).
  - Példa: `/help`

----------------------------------------
2. Időjárás lekérdezés

- /idő vagy !idő
  - Paraméterek:
    - helyszín: <string> — város vagy település neve (pl. Budapest)
    - egység: [metric/imperial] — opcionális, alapértelmezett: metric
  - Példa (slash): `/idő helyszín:Budapest`
  - Példa (prefix): `!idő Budapest`
  - Visszaadott mezők:
    - Állapot (pl. Felhős, Esős)
    - Hőmérséklet (°C) és érzet
    - Páratartalom %
    - Szél (m/s vagy km/h)
    - Nyomás (hPa)
    - Rövid öltözködési javaslat (lásd Öltözködés parancs)

- /idő részletes vagy !idő -d
  - Leírás: Részletes információ (óránkénti előrejelzés, napkelte/napnyugta)
  - Paraméterek: ugyanazok, plusz: részletek: [hourly/daily/all]

----------------------------------------
3. Öltözködési tanácsok

- /mitvegyekfol vagy !mitvegyekfol
  - Paraméterek:
    - helyszín: <string>
    - gender: [auto/none/masculine/feminine] — opcionális
  - Példa: `/mitvegyekfol helyszín:Szeged gender:auto`
  - Leírás: A bot a jelenlegi időjárás alapján javasol ruházatot, figyelembe véve hőmérsékletet, csapadékot és szelet.

----------------------------------------
4. Játékok

- /tippelj vagy !tippelj
  - Paraméterek:
    - nehézség: [easy/medium/hard]
  - Leírás: A bot megjelenít időjárási statisztikákat (bizonyos információk elrejtve), a játékosnak ki kell találnia a várost.
  - Parancsok játék közben:
    - /hint — segítség
    - /feladás — feladom

- /vicc vagy !vicc
  - Leírás: Véletlenszerű, időjáráshoz kapcsolódó vicc visszaadása.
  - Példa: `/vicc`

----------------------------------------
5. Összehasonlító parancsok

- /osszehasonlit vagy !osszehasonlit
  - Paraméterek:
    - varos1: <string>
    - varos2: <string>
  - Leírás: Két város időjárásának összevetése (hőmérséklet, páratartalom, szél, stb.)
  - Példa: `/osszehasonlit varos1:Budapest varos2:Szeged`

- /legmelegebb vagy !legmelegebb
  - Leírás: Megkeresi a legmelegebb várost a mintában vagy a támogatott listában.
  - Paraméterek: [minta_meret] — hány várost vizsgáljon (opcionális)

- /leghidegebb vagy !leghidegebb
  - Leírás: Fordított művelet a leghidegebb városra.

----------------------------------------
6. Nyelv és lokalizáció

- /nyelv vagy !nyelv
  - Paraméterek:
    - language: [hu/en]
  - Leírás: Felhasználó preferált nyelve beállítása.
  - Példa: `/nyelv language:hu`

----------------------------------------
7. Hibakezelés és jogosultságok

- Hibák:
  - "Invalid token" — ellenőrizd a DISCORD_TOKEN környezeti változót.
  - "API call failed" — ellenőrizd az OpenWeatherMap kulcsot és a rate limitet.
  - "City not found" — javasolt tippek: városnév pontosítása, alternatív név megadása.

- Jogosultságok:
  - Általában nincs szükség különleges jogosultságra a legtöbb parancshoz.
  - Admin-only parancsok (ha léteznek, pl. bot restart, statisztikák) — csak a bot tulajdonosa / maintainer szerepekkel használhatók.

----------------------------------------
8. Parancs kiterjesztés — sablon fejlesztőknek

- Slash parancs (discord.py 2.x / app commands) példa:
```py
@bot.tree.command(name="idő", description="Aktuális időjárás egy megadott városra")
@app_commands.describe(helyszin="Város neve, pl. Budapest", egseg="metric vagy imperial")
async def ido(interaction: discord.Interaction, helyszin: str, egseg: str = "metric"):
    await interaction.response.defer()
    data = await weather.get_current(helyszin, units=egseg)
    await interaction.followup.send(format_weather(data))
```

- Prefix parancs (klasszikus) példa:
```py
@bot.command(name="idő", aliases=["ido", "weather"])
async def ido_cmd(ctx, *, helyszin: str):
    data = await weather.get_current(helyszin)
    await ctx.send(format_weather(data))
```

- Új parancs hozzáadásának lépései:
  1. Készíts egy új Python fájlt a `cogs/` (vagy `commands/`) mappába (ha nincs ilyen, javasoljuk létrehozni).
  2. Kövesd a projekt kódstílusát (PEP8), írj docstring-et.
  3. Adj hozzá egység- vagy integrációs tesztet (ha lehetséges).
  4. Nyiss egy Pull Requestet, és töltsd ki a PR leírásában, milyen funkciót ad hozzá és hogyan tesztelhető.

----------------------------------------
9. Verziózás és kompatibilitás

- A bot Python 3.8+-on fut (README alapján).
- Mindig ellenőrizd a requirements.txt-ben szereplő csomagok verzióját, ha új csomagot adsz hozzá, mérlegeld a függőségeket.

----------------------------------------
10. Gyakori kérdések (FAQ)

- Hogyan adok hozzá új városlistát?
  - A HUNGARIAN_CITIES lista a main.py-ben található (README említése szerint). Ha nagy listát adsz hozzá, győződj meg róla, hogy az API-hívások hatékonyak (cache vagy rate-limiting).

- Hogyan lokalizálom a parancsokat más nyelvekre?
  - Használj belső fordító táblázatot (pl. i18n.json), és a parancsokban válaszd a megfelelő nyelvi stringeket a felhasználó beállítása alapján.

----------------------------------------
Végszó
Ha szeretnéd, segítek ezt a fájlt közvetlenül hozzáadni a `docs/` mappához a repódban, vagy elkészítem belőle a PR-diffet, amit te alkalmazhatsz.
