import pandas as pd
from bs4 import BeautifulSoup
import requests


# Headers are hardcoded as provided
header = ['No', 'Teams', 'G', 'Min', 'Pts', 'Reb', 'Ast', 'Stl', 'Blk', 'To', 'Pf', 'Dreb', 'Oreb', 'Fgm-a', 'Pct', '3gm-a', 'Pct', 'Ftm-a', 'Pct', 'Eff', 'Deff']


def scrape_table_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')


        # Find all tables with the 'statscontent' class for content
        content_tables = soup.find_all('table', class_='statscontent')
        content = []
        for table in content_tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    content.append([cell.get_text(strip=True) for cell in cells])

        return content
    else:
        print(f"Failed to retrieve page from {url}. Status code: {response.status_code}")
        return []

# URL to scrape
url = 'http://www.hoopsstats.com/basketball/fantasy/nba/teamstats'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# Function call
content = scrape_table_data(url, headers)

# Now, header contains the header of the table and content contains each row of the table body
print("Headers:", header)
for row in content:
    print("Row:", row)

# Save to CSV
df = pd.DataFrame(content, columns=header)
df.to_csv('stats_data.csv', index=False)
print("Data has been saved to stats_data.csv")
