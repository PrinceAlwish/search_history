from bs4 import BeautifulSoup
import pandas as pd

def extract_search_history(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    searches = []

    for div in soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'):
        text = div.get_text(strip=True)
        if 'Searched for' in text:
            search_term = text.replace('Searched for ', '')
            searches.append(search_term)

    return searches

def save_to_excel(searches, output_file):
    df = pd.DataFrame(searches, columns=['Search Query'])
    df.to_excel(output_file, index=False)
    print(f"Saved {len(searches)} search queries to {output_file}")

if __name__ == '__main__':
    file_path = 'MyActivity.html'
    output_file = 'SearchHistory.xlsx'

    history = extract_search_history(file_path)
    save_to_excel(history, output_file)
