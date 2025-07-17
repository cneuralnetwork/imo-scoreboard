import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://local.imo-official.org/Mboards/Scoreboard.aspx?page={page}&dimX=4&dimY=3&time=10"
PAGES = range(1, 11)

results = []

for page in PAGES:
    url = BASE_URL.format(page=page)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Find the main scoreboard table (the one containing all the team tables)
    main_table = soup.find('table', style=lambda v: v and 'border' in v)
    if not main_table:
        continue
    # Find all <table> elements inside the main table (each is a team/column)
    team_tables = main_table.find_all('table')
    for team_table in team_tables:
        tbody = team_table.find('tbody')
        if not tbody:
            continue
        for row in tbody.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) != 8:
                continue  # skip malformed rows
            code = cells[0].get_text(strip=True)
            # Parse P1-P6, treat empty or '•' as 0, and count checked
            scores = []
            checked = 0
            for i in range(1, 7):
                val = cells[i].get_text(strip=True)
                if val == '' or val == '\u2022' or val == '•':
                    scores.append(0)
                else:
                    checked += 1
                    try:
                        scores.append(int(val))
                    except Exception:
                        scores.append(0)
            # Parse total
            total_val = cells[7].get_text(strip=True)
            try:
                total = int(total_val)
            except Exception:
                total = 0
            results.append({
                'country': code,
                'P1': scores[0],
                'P2': scores[1],
                'P3': scores[2],
                'P4': scores[3],
                'P5': scores[4],
                'P6': scores[5],
                'total': total,
                'checked': checked
            })

# Remove duplicates (some codes may appear on multiple pages)
unique_results = {r['country']: r for r in results}
final_results = list(unique_results.values())

# Sort by total descending
final_results.sort(key=lambda x: x['total'], reverse=True)

# Aggregate by country (first 3 letters of code)
country_totals = {}
country_counts = {}
country_checked = {}
for r in final_results:
    country = r['country'][:3]
    country_totals[country] = country_totals.get(country, 0) + r['total']
    country_counts[country] = country_counts.get(country, 0) + 1
    country_checked[country] = country_checked.get(country, 0) + r['checked']

country_results = [
    {'country': c, 'total': country_totals[c], 'num_contestants': country_counts[c], 'checked': country_checked[c]}
    for c in country_totals
]
country_results.sort(key=lambda x: x['total'], reverse=True)

with open('scoreboard.json', 'w') as f:
    json.dump(final_results, f, indent=2)

with open('country_scoreboard.json', 'w') as f:
    json.dump(country_results, f, indent=2)

print(f"Scraped {len(final_results)} contestants. Data saved to scoreboard.json.")
print(f"Aggregated {len(country_results)} countries. Data saved to country_scoreboard.json.") 