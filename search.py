from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

def extract_search_history(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    searches = []

    entries = soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')

    for entry in entries:
        text = entry.get_text(strip=True)

        if text.startswith('Searched for'):
            # Remove "Searched for"
            text = text.replace('Searched for', '', 1).strip()

            # Extract the datetime part using regex (date followed by time)
            match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}:\d{2}\s*[AP]M', text)

            if match:
                datetime_str = match.group(0)
                try:
                    dt_obj = datetime.strptime(datetime_str, '%b %d, %Y, %I:%M:%S %p')
                except ValueError:
                    continue  # Skip if datetime format doesn't match

                search_query = text.replace(datetime_str, '').strip()

                searches.append({
                    'Searched For': search_query,
                    'Date': dt_obj.strftime('%B %d, %Y'),
                    'Time': dt_obj.strftime('%I:%M %p')
                })

    return searches

def save_to_excel(searches, output_file):
    df = pd.DataFrame(searches)
    df.to_excel(output_file, index=False)
    print(f"Saved {len(searches)} search entries to {output_file}")

if __name__ == '__main__':
    file_path = 'MyActivity.html'  # Replace with your actual file path
    output_file = 'SearchHistory.xlsx'

    history = extract_search_history(file_path)
    save_to_excel(history, output_file)
