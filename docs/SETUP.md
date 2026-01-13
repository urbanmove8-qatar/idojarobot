# Telepítés (rövid)

1. Klónozd a repót:
```bash
git clone https://github.com/urbanmove8-qatar/idojarobot.git
cd idojarobot
```

2. Virtuális környezet:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Telepítés:
```bash
pip install -r requirements.txt
```

4. Konfiguráció:
- Másold a `.env.example` fájlt `.env` néven és töltsd ki a szükséges kulcsokat (DISCORD_TOKEN, WEATHER_API_KEY).

5. Futtatás:
```bash
python main.py
```
