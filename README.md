# Engeto_python_projekt_3: Election Scraper

Třetí projekt pro kurz Datový analytik s Pythonem.

## Popis projektu

Tento skript umožňuje stáhnout kompletní výsledky z parlamentních voleb v roce 2017 pro zvolený územní celek (okres) a všechny jeho obce z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Data jsou následně uložena do CSV souboru ve strukturovaném formátu.

### Výstupní data obsahují:

- Kód obce
- Název obce
- Počet registrovaných voličů
- Počet vydaných obálek
- Počet platných hlasů
- Výsledky hlasování pro jednotlivé kandidující strany
  
## Instalace knihoven

Knihovny použité v kódu a jejich verze jsou uloženy do souboru requirements.txt. Pro instalaci je vhodné použít nové virtuální prostředí a v IDE spustit následovně:

```bash
pip install -r requirements.txt
```

## Spuštění projektu

Program se spouští s **2 povinnými argumenty**:

```bash
python main.py <URL_uzemniho_celku> <nazev_vysledneho_souboru.csv>
```

### Argumenty:

1. **URL územního celku** - odkaz na vybraný okres z [hlavní stránky voleb](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
2. **Název výstupního souboru** - název CSV souboru, do kterého se uloží výsledky (musí končit `.csv`)

## Ukázka použití

Příklad pro okres Nový Jičín:

**1. Zadání argumentů:**

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104
2. argument: novy_jicin_volby.csv

**2. Spusť skript:**

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104" "vysledky_novy_jicin.csv"
```

**3. Průběh stahování:**

```
==================================================
SCRAPER VÝSLEDKŮ VOLEB 2017
==================================================

URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8104
Výstupní soubor: novy_jicin_volby.csv

Stahuji seznam obcí...
Nalezeno obcí: 54

Stahuji data pro: Albrechtičky (568741)
Stahuji data pro: Bartošovice (599212)
Stahuji data pro: Bernartice nad Odrou (568481)
Stahuji data pro: Bílov (546984)
...
Stahuji data pro: Životice u Nového Jičína (547000)

Data úspěšně uložena do: novy_jicin_volby.csv
Celkem obcí: 54

==================================================
HOTOVO!
==================================================
```

**4. Částečný výstup CSV souboru:**

Soubor `vysledky_novy_jicin.csv` bude obsahovat data ve formátu:

| code   | location      | registered | envelopes | valid | Občanská demokratická strana | Řád národa - Vlastenecká unie | ... |
|--------|---------------|------------|-----------|-------|------------------------------|-------------------------------|-----|
| 598917 | Albrechtičky  | 794        | 493       | 491   | 61                           | 0                             | ... |
| 511129 | Bartošovice   | 1578       | 960       | 953   | 85                           | 0                             | ... |
| 598925 | Bílovec       | 6184       | 3807      | 3802  | 250                          | 3                             | ... |


## Chyby

Program kontroluje:

- **Počet argumentů** - musí být zadány právě 2 argumenty
- **Validitu URL** - odkaz musí začínat `https://www.volby.cz/pls/ps2017nss/ps32`
- **Příponu souboru** - výstupní soubor musí mít příponu `.csv`
- **Dostupnost stránek** - pokud se nepodaří stáhnout data, program skončí s chybovou hláškou

