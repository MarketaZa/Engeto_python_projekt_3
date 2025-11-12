"""Scraper výsledků voleb 2017 - scraping dat z volby.cz"""

import csv
import sys
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup

def validate_arguments() -> Tuple[str, str]:
    """Validuje argumenty příkazové řádky."""
    if len(sys.argv) != 3:
        print("CHYBA: Musíte zadat právě 2 argumenty: <url> <output.csv>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2]
    
    if not url.startswith("https://www.volby.cz/pls/ps2017nss/ps32"):
        print("CHYBA: Neplatný odkaz!")
        sys.exit(1)
    
    if not output_file.endswith(".csv"):
        print("CHYBA: Výstupní soubor musí mít příponu .csv")
        sys.exit(1)
    
    return url, output_file

def fetch_page(url: str) -> BeautifulSoup:
    """Stáhne HTML stránku a vrátí BeautifulSoup objekt."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"CHYBA: Nepodařilo se stáhnout stránku: {e}")
        sys.exit(1)

def extract_municipality_links(soup: BeautifulSoup) -> List[Tuple[str, str, str]]:
    """Extrahuje odkazy na jednotlivé obce z přehledové stránky."""
    municipalities = []
    tables = soup.find_all('table', {'class': 'table'})
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows[2:]:
            cells = row.find_all('td')
            
            if len(cells) >= 3:
                code_cell = cells[0]
                code = code_cell.get_text(strip=True)
                
                name_cell = cells[1]
                name = name_cell.get_text(strip=True)
                
                link_cell = cells[0]
                link_tag = link_cell.find('a')
                
                if link_tag and code and name:
                    relative_url = link_tag.get('href')
                    full_url = f"https://www.volby.cz/pls/ps2017nss/{relative_url}"
                    municipalities.append((code, name, full_url))
    
    return municipalities

def extract_voting_data(soup: BeautifulSoup) -> Dict[str, str]:
    """Extrahuje základní volební data (voliči, obálky, hlasy)."""
    data = {}
    tables = soup.find_all('table', {'class': 'table'})
    
    if len(tables) >= 1:
        rows = tables[0].find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            headers = row.find_all('th')
            
            if len(cells) >= 3:
                data['registered'] = cells[3].get_text(strip=True)
                data['envelopes'] = cells[4].get_text(strip=True)
                data['valid'] = cells[7].get_text(strip=True)
                break
    
    return data

def extract_party_results(soup: BeautifulSoup) -> Dict[str, str]:
    """Extrahuje výsledky hlasování pro jednotlivé strany."""
    parties = {}
    tables = soup.find_all('table', {'class': 'table'})
    
    for table in tables[1:]:
        rows = table.find_all('tr')
        
        for row in rows[2:]:  
            cells = row.find_all('td')
            
            if len(cells) >= 3:
                party_name = cells[1].get_text(strip=True)
                votes = cells[2].get_text(strip=True)
                
                if party_name and votes and any(char.isdigit() for char in votes):
                    parties[party_name] = votes
    
    return parties

def scrape_municipality(code: str, name: str, url: str) -> Dict[str, str]:
    """Scrapuje data pro jednu obec."""
    print(f"Stahuji data pro: {name} ({code})")
    
    soup = fetch_page(url)
    
    result = {
        'code': code,
        'location': name
    }
    
    voting_data = extract_voting_data(soup)
    result.update(voting_data)
    
    party_results = extract_party_results(soup)
    result.update(party_results)
    
    return result

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    if not data:
        print("VAROVÁNÍ: Žádná data k uložení!")
        return
    
    all_keys = []
    for row in data:
        for key in row.keys():
            if key not in all_keys:
                all_keys.append(key)
    
    ordered_keys = ['code', 'location', 'registered', 'envelopes', 'valid']
    party_keys = [k for k in all_keys if k not in ordered_keys]
    ordered_keys.extend(sorted(party_keys))
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ordered_keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"\nData úspěšně uložena do: {filename}")
        print(f"Celkem obcí: {len(data)}")
    
    except IOError as e:
        print(f"CHYBA: Nepodařilo se uložit soubor: {e}")
        sys.exit(1)

def main() -> None:
    """Hlavní funkce programu."""
    print("=" * 50)
    print("SCRAPER VÝSLEDKŮ VOLEB 2017")
    print("=" * 50)
    
    url, output_file = validate_arguments()
    
    print(f"\nURL: {url}")
    print(f"Výstupní soubor: {output_file}")
    print("\nStahuji seznam obcí...")
    
    soup = fetch_page(url)
    municipalities = extract_municipality_links(soup)
    
    if not municipalities:
        print("CHYBA: Nepodařilo se najít žádné obce!")
        sys.exit(1)
    
    print(f"Nalezeno obcí: {len(municipalities)}\n")
    
    all_data = []
    
    for code, name, mun_url in municipalities:
        try:
            mun_data = scrape_municipality(code, name, mun_url)
            all_data.append(mun_data)
        except Exception as e:
            print(f"VAROVÁNÍ: Chyba při zpracování {name}: {e}")
            continue
    
    save_to_csv(all_data, output_file)
    
    print("\n" + "=" * 50)
    print("HOTOVO!")
    print("=" * 50)

if __name__ == "__main__":
    main()