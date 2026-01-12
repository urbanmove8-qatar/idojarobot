# 🌤️ Időjáróbot

![Discord.py](https://img.shields.io/badge/discord.py-latest-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)
![Status](https://img.shields.io/badge/Status-Aktív-brightgreen.svg)

**Időjáróbot** - A legjobbak közé tartozó, teljes funkcionalitású Discord bot a magyar időjárás lekérdezéséhez, amely reklámmentes, gyors és megbízható.

## 🎯 Jellemzők

### 🌡️ Valós idejű Időjárási Adatok
- **Aktuális időjárás**: Hőmérséklet, páratartalom, szélsebesség, nyomás
- **Széles város választék**: 80+ magyar város és község támogatása
- **OpenWeatherMap API**: Megbízható és naprakész adatok
- **Gyors lekérdezés**: Azonnali eredmények milliszekundumos válaszidővel

### 👕 Intelligens Öltözködési Tanácsok
- **Hőmérséklet alapú javaslatok**: Automatikus outfit ajánlás az időjárás függvényében
- **Nemi specifikus tanácsok**: Saját javaslatok nőknek és férfiaknak
- **Időjárási feltételek figyelembevétele**: Esőre, hóra, széltől függő extra tippek
- **Érzelmes emoji zörgás**: 😊 Barátságos és interaktív kommunikáció

### ⚠️ Intelligens Időjárás Figyelmeztetések (HungaroMet stílusú)
- **Hőségriasztás**: Extrém meleg esetén vészjelzés 🔴
- **Hideg riasztás**: Szélsőséges hideg figyelmeztetés 🔵
- **Viharjelzés**: Zivatar és erős szél előjelzése ⚡
- **Havazási figyelmeztetés**: Téli közlekedés veszélyei ❄️
- **Érzelmes és vizuális**: Hangulat emojikkal feldúsított figyelmeztetések 😭😱😳

### 🎮 Szórakoztató Játékok
- **Melyik város ez?**: Időjárási adatok alapján kitalálod a várost
- **3 nehézségi szint**: Könnyű, közepes, nehéz játékmódok
- **Hint rendszer**: Szegmentális segítség a játékosoknak
- **Multiplayer támogatás**: Több játékos egy csatornában

### 📊 Összehasonlító Elemzés
- **Két város összehasonlítása**: Hőmérséklet, páratartalom, időjárás eltérések
- **Legmelegebb város**: Automatikus megkeresés az összes magyar város közül
- **Leghidegebb város**: Fordított keresés a leghidegebb helyre
- **Vizuális ranking**: Egyértelmű különbség megjelenítés

### 🗺️ Hasznos Linkek
- **OpenWeatherMap térkép**: Interaktív világtérkép
- **Met.hu**: Magyar Meteorológiai Szolgálat
- **Időkép.hu**: Nép szerű magyar időjárás oldal
- **Windy**: Professzionális szélanalízis

### 😄 Szórakoztató Viccek
- **27+ Időjárás vicc**: Programozós, meteorológiai és általános viccek
- **Véletlen vicc**: Minden nap más vicc a `/vicc` paranccsal

### 🌍 Multilingvális Támogatás
- **Magyar nyelvű teljes felhasználói felület** 🇭🇺
- **Angol nyelvű támogatás** 🇬🇧 (felhasználók választhatnak a `/nyelv` parancssal)
- **Helyi fordítások**: Város nevek és időjárás leírások eredeti nyelven

---

## 🚀 Gyors Indulás

### 1️⃣ Előfeltételek
- Python 3.8 vagy magasabb
- pip (Python Package Manager)
- Discord bot token
- OpenWeatherMap API kulcs

### 2️⃣ Telepítés

1. **Repository klónozása**:
   ```bash
   git clone https://github.com/urbanmove/idojarobot.git
   cd idojarobot
   ```

2. **Virtuális környezet létrehozása** (ajánlott):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Függőségek telepítése**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurálás**:
   - Nyisd meg a `main.py` fájlt
   - Keress a `# --- CONFIGURATION ---` szekcióra
   - Pótold az alábbi értékeket:
     ```python
     DISCORD_TOKEN = "your_discord_bot_token_here"
     WEATHER_API_KEY = "your_openweathermap_api_key_here"
     ```

5. **Bot elindítása**:
   ```bash
   python main.py
   ```

---

## 📋 Parancsok

### 🌡️ Időjárás Lekérdezés

**Slash parancs**:
```
/idő helyszín:Budapest
```

**Prefix parancs**:
```
!idő Budapest
```

**Válasz**:
```
🌡️ Időjárás: Budapest
Állapot: Felhős
Hőmérséklet: 15.2°C (Érzet: 12.8°C)
Páratartalom: 65% | Szél: 12.3 m/s | Nyomás: 1013 hPa
👕 Mit vegyek föl?: Kabát vagy dzseki, pulóver
```

---

### 👔 Öltözködési Tanácsok

**Slash parancs**:
```
/mitvegyekfol helyszín:Szeged
```

**Függvénysége**: Teljes öltözködési javaslatot ad a jelenlegi időjárás alapján, nem elég a hőmérséklet!

---

### 🎮 Tippelő Játék - "Melyik Város Ez?"

**Slash parancs**:
```
/tippelj nehézség:medium
```

**Nehézségi szintek**:
- 🟢 **Könnyű**: Teljes hőmérséklet, időjárás, páratartalom + hint
- 🟡 **Közepes**: Hőmérséklet tartomány és időjárás
- 🔴 **Nehéz**: Körülbelüli hőmérséklet és páratartalom

**Játékmechanika**:
1. A bot egy véletlenszerű város időjárási adatait mutatja
2. Te tippelsz a város nevével
3. `/hint` - Segítség kérése (hosszú betűk, régió stb.)
4. `/feladás` - Feladni a játékot

---

### ⚖️ Városok Összehasonlítása

**Slash parancs**:
```
/osszehasonlit város1:Budapest város2:Szeged
```

**Megjeleníti**:
- Hőmérséklet különbség
- Időjárási feltételek összehasonlítása
- Páratartalom eltérések
- Melyik város melegebb

---

### 🔥 Legmelegebb Város

**Slash parancs**:
```
/legmelegebb
```

Megkeresi a **legmelegebb magyar várost** (15 város véletlenszerű mintájából).

---

### ❄️ Leghidegebb Város

**Slash parancs**:
```
/leghidegebb
```

Megkeresi a **leghidegebb magyar várost** az időjárási adatok alapján.

---

### 🌍 Nyelv Beállítás

**Slash parancs**:
```
/nyelv language:hu
```

**Lehetőségek**:
- `hu` - Magyar 🇭🇺
- `en` - Angol 🇬🇧

---

### ℹ️ Bot Információ

**Parancs**:
```
/info
```

**Megjelenít**:
- Bot verzió
- Szerverek száma
- API forrás
- Támogatott városok száma

---

### 🏓 Ping / Válaszidő

**Parancs**:
```
/ping
```

**Válasz**: Milliszekundumos válaszidő (ms)

---

### 😄 Vicc

**Parancs**:
```
/vicc
```

**Vissza ad**: Egy random magyar nyelvű időjárás vicc 😂

---

### 🗺️ Térképek

**Parancs**:
```
/terkep
```

**Linkek**:
- OpenWeatherMap interaktív térkép
- Met.hu - Magyar Meteorológiai Szolgálat
- Időkép.hu - Népszerű magyar app
- Windy - Professzionális szél analízis

---

### 📖 Segítség

**Parancs**:
```
/help
```

Megjeleníti az összes elérhető parancs teljes listáját.

---

## 📦 Támogatott Magyar Városok

80+ város, beleértve:

**Nagyvárosok**: Budapest, Debrecen, Szeged, Miskolc, Pécs, Győr, Nyíregyháza, Kecskemét, Székesfehérvár, Szombathely

**Regionális városok**: Eger, Tatabánya, Sopron, Veszprém, Békéscsaba, Zalaegerszeg

**Kis községek**: Siófok, Keszthely, Tihany, Balatonfüred, Vonyarcvashegy, Révfülöp és még sok más...

Teljes lista a `main.py`-ben: `HUNGARIAN_CITIES` lista.

---

## 🔒 Biztonság & Adatvédelem

### ✅ Biztonsági Intézkedések
- **Token megóvás**: Gitignore-ban vannak az API kulcsok
- **Input validáció**: Város nevek ellenőrzése
- **Rate limiting**: OpenWeatherMap API limiteinek tisztelete
- **Hiba kezelés**: Robusztus error handling minden API híváshoz

### 📋 Adatkezelés
- **Feldolgozás**: Csak a szükséges adatokat tárolunk
- **Tárolás**: Felhasználók játék adatai memóriában (nem perzisztens)
- **Adatvédelem**: Nincs felhasználói email vagy személyes adat tárolása
- **GDPR**: Teljes GDPR megfelelőség

---

## 🛠️ Fejlesztői Útmutató

### Projektszerkezet
```
idojarobot/
├── main.py                 # Fő bot kód
├── requirements.txt        # Python függőségek
├── .gitignore             # Gitignore (API kulcsok)
├── .env.example           # Environment template
├── README.md              # Ez a fájl
├── LICENSE                # Apache 2.0
└── docs/
    ├── SETUP.md           # Részletes telepítési útmutató
    ├── COMMANDS.md        # Parancsok dokumentáció
    └── CONTRIBUTING.md    # Hozzájárulási szabályok
```

### Kódstilus
- PEP 8 követés
- Szélességi korlát: 120 karakter
- Snake_case függvények és változók
- Dokumentáló stringek (docstrings) minden függvényen

### Új parancsok hozzáadása

**Slash parancs**:
```python
@bot.tree.command(name="új_parancs", description="Parancs leírása")
@app_commands.describe(param="Paraméter leírása")
async def new_command(interaction: discord.Interaction, param: str):
    """Parancs dokumentáció."""
    await interaction.response.defer()
    # Kód itt
    await interaction.followup.send("Válasz", ephemeral=False)
```

**Prefix parancs**:
```python
@bot.command(name='új_parancs', aliases=['alias1', 'alias2'])
async def new_prefix_command(ctx, *, param: str):
    """Parancs dokumentáció."""
    # Kód itt
    await ctx.send("Válasz")
```

---

## 📊 Bot Statisztikák

- **Lehetséges parancsok**: 20+
- **Támogatott városok**: 80+
- **Fordítások**: 2 (Magyar, Angol)
- **Játékok**: 1 (Város tippelős)
- **Viccek**: 27+
- **Válaszidő**: < 500ms átlagban
- **Uptime**: 99.9% (remélhetőleg!)

---

## 🐛 Ismert Problémák & Workaroundok

### OpenWeatherMap API
- **Probléma**: "API call failed" üzenet
- **Megoldás**: Ellenőrizd az API kulcsot és a Rate limiteket
- **Dokumentáció**: https://openweathermap.org/api

### Discord Token
- **Probléma**: "Invalid token" hiba
- **Megoldás**: Frissítsd a bot tokenjet a Discord Developer Portalon
- **Link**: https://discord.com/developers/applications

### Python Verzió
- **Probléma**: Szintaxis hiba a futtatásnál
- **Megoldás**: Python 3.8+ szükséges (`python --version`)

---

## 🤝 Közreműködés

Szeretnél segíteni? Nagyszerű! 🎉

### Hogyan járulj hozzá:

1. **Forkold a repo-t**
   ```bash
   git clone https://github.com/yourusername/idojarobot.git
   ```

2. **Hozz létre egy feature branch-et**
   ```bash
   git checkout -b feature/new-feature
   ```

3. **Commit a módosításokat**
   ```bash
   git commit -m "Add new feature: [description]"
   ```

4. **Push a branch-hez**
   ```bash
   git push origin feature/new-feature
   ```

5. **Nyiss egy Pull Request**

### Közreműködési szabályok
- ✅ Követni kell a PEP 8 stílust
- ✅ Dokumentálni kell az új paramétereket
- ✅ Magyar és angol verzió mindkettő szükséges
- ✅ Tesztelni kell a módosításokat

---

## 📝 Licenc

Ez a projekt **Apache License 2.0** alatt áll.

```
Copyright 2025 Urbanmove 8 Kft.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

Teljes licenc: [LICENSE](LICENSE) fájl

---

## 📞 Támogatás & Kapcsolat

### Problémáid vannak?

1. **GitHub Issues**: Nyiss egy issue ezt: https://github.com/urbanmove/idojarobot/issues
2. **Email**: support@urbanmove.hu
3. **Discord**: Csatlakozz a Discord szerverekhez
4. **Documentation**: Olvasd el a [docs/](docs/) mappát

### Válaszidő
- **Bug jelentés**: 24 óra
- **Feature request**: 48 óra
- **Egyéb kérdés**: 72 óra

---

## 🌟 Köszönet

- **OpenWeatherMap** - Ingyenes és megbízható API
- **discord.py** - Kitűnő Discord könyvtár
- **A magyar közösségnek** - Az ötletekért és tesztekért
- **Te** - A bot használatáért! ❤️

---

## 📈 Roadmap

### v1.1 (Tervezett)
- [ ] Több város egyidejű lekérdezése
- [ ] Csillagászati adatok (Hold fázisa, bolygók)
- [ ] Naptarisztikai adatok (napfelkelte, napnyugta)
- [ ] Riasztás beállítási peristenciálás

### v1.2 (Tervezett)
- [ ] Saját Discord bot dashboard
- [ ] Nemzetközi város támogatás
- [ ] Időjárási grafikon generálás
- [ ] Múlt béli adatok lekérdezése

### v2.0 (Jövőbeni)
- [ ] MongoDB integráció
- [ ] Webes felület
- [ ] WebHook támogatás
- [ ] Prémium funkciók

---

## 🎓 Tanulási Erőforrások

- **discord.py dokumentáció**: https://discordpy.readthedocs.io/
- **OpenWeatherMap API**: https://openweathermap.org/api
- **Python dokumentáció**: https://docs.python.org/3/
- **GitHub Git oktatóanyag**: https://guides.github.com/

---

## ✨ Legutóbbi Frissítések

### v1.0.0 (2025-01-12) ✅
- ✨ Teljes bot funkcionalitás
- 🌍 Slash parancsok támogatása
- 🎮 Város tippelős játék
- 👕 Öltözködési tanácsadó
- ⚠️ HungaroMet stílusú figyelmeztetések
- 🌍 80+ magyar város támogatása
- 🌐 Kétnyelvű felhasználói felület

---

**Készült ❤️ által az Urbanmove 8 Kft. csapatával**

🇭🇺 **MAGYAR PROUDLY** 🇭🇺

---

*Last updated: 2025-01-12*
*Version: 1.0.0*
