# Hozzájárulási útmutató (CONTRIBUTING)

Köszönjük, hogy hozzájárulnál az Időjáróbot projekthez! Itt találod a legfontosabb szabályokat, lépéseket és elvárásokat a gördülékeny közreműködéshez.

1) Alapok
- Forkold a repót és dolgozz a saját fork-odon.
- Kérjük, kövesd a projekt stílusát (PEP 8), adj docstringeket és írj teszteket, ahol lehetséges.
- Mielőtt PR-t nyitsz, győződj meg róla, hogy a kódod fut és a linter nem jelez súlyos hibákat.

2) Fejlesztői környezet beállítása
```bash
git clone https://github.com/<your-username>/idojarobot.git
cd idojarobot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# fejlesztői eszközök (opcionális)
pip install -r requirements-dev.txt  # ha van ilyen
```

3) Branch stratégia és commit üzenetek
- Branch név: `feature/<rövid-leírás>`, `bugfix/<rövid-leírás>` vagy `chore/<leírás>`
- Commit üzenetek legyenek tömörek és informatívak. Használhatsz konvenciót: `feat:`, `fix:`, `docs:`, `chore:`, `test:` stb.
  - Példa: `feat: add /vicc command with jokes list`

4) Issue-k és PR-ek
- Ha hibát találsz, nyiss egy Issue-t a `bug` sablonnal (ha létezik).
- PR leírása tartalmazzon:
  - Rövid összefoglaló mit változtat a PR
  - Milyen teszteket futtattál
  - Ha releváns, migrációs vagy konfigurációs változtatások
- PR-eknél várható review: fenntartó(k) átnézik. Kisebb PR-eket gyorsabban merge-lünk.

5) Kódstílus és minőség
- Kövesd a PEP 8 szabályait (max line length a projektben: 120, vagy a pyproject-ban meghatározott).
- Formázó/ellenőrző eszközök:
  - black
  - isort
  - flake8
  - mypy (opcionális típusellenőrzés)
- Javasolt: telepítsd a pre-commit hookokat:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

6) Tesztek
- Minden új funkcióhoz vagy bugfixhez jó, ha tartozik teszt.
- Tesztek futtatása:
```bash
pytest -q
```
- Egyszerű smoke tesztek telepítve vannak a `tests/` mappában (ha van).

7) Biztonság és titkos adatok
- Semmilyen PR-ben ne tegyél közzé titkos kulcsokat (DISCORD_TOKEN, WEATHER_API_KEY stb.).
- Ha véletlenül kiszivárgott egy kulcs, azonnal rotáld (új token a szolgáltatásban), és jelezd a repo fenntartójának.

8) Hozzáadás: új parancs / funkció
- Készíts külön branchet.
- Add hozzá a parancsot `cogs/` vagy `commands/` mappában (ha nincs, beszéljük meg a struktúrát).
- Írj egy rövid dokumentációs részt a `docs/COMMANDS.md`-hez.
- Adj hozzá legalább egy alap tesztet, ahol lehetséges.
- Készíts PR-t a `main` branch felé.

9) Fordítások és lokalizáció
- Szöveges stringeket tartsd külön fájlban (pl. `i18n/hu.json`, `i18n/en.json`) a könnyebb szerkeszthetőségért.
- Ha új stringet adsz hozzá, ellenőrizd mindkét nyelvi fájlt, hogy konzisztensek maradjanak.

10) Kapcsolat és támogatás
- PR-ekkel/issue-kkal kapcsolatos kérdések: használd a GitHub Issue rendszert.
- Vészhelyzet vagy biztonsági hiba: nézd meg a SECURITY.md fájlt és kövesd az ott leírtakat (ne jelentsd a hibát nyilvánosan).
- Ha szeretnél közvetlenebb kommunikációt: robloxurbanmove8@gmail.com vagy a projekt Discord szervere (README-ban található link).

11) Köszönjük!
Köszönjük, hogy időt szánsz a közreműködésre. Minden hozzájárulás értékes — még a dokumentációs javítások is!

----------------------------------------
Gyors ellenőrző lista PR-hez
- [ ] Kód stílusa megfelel (pre-commit futtatva)
- [ ] Tesztek futnak (pytest)
- [ ] README / docs frissítve, ha szükséges
- [ ] Nincs titkos adat a commitokban
- [ ] PR leírás világos és rövid

----------------------------------------
Sablon: egyszerű PR leírás
```
### Mit csinál ez a PR?
Röviden: (pl. "Hozzáadja a /vicc parancsot, amely random viccet ad vissza")

### Tesztelés
- `pytest` lefutott
- Manuális teszt: `/vicc` a teszt szerveren

### Megjegyzés
(ha van)
```

Végezetül: ha szeretnéd, elkészítem a fenti fájlokhoz PR-t a repódhoz, vagy generálok egy patch fájlt, amit te tudsz alkalmazni. Melyiket szeretnéd?
