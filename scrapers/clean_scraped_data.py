import json
import re
from urllib.parse import urlparse, unquote

def is_null_indicator(value, null_indicators):
    return value.lower() in null_indicators

def remove_null_indicators(data, null_indicators):
    for key, value in data.items():
        if key == 'LanguageName':
            continue  # Skip LanguageName

        if isinstance(value, list):
            data[key] = [v for v in value if not is_null_indicator(v, null_indicators)]
        elif isinstance(value, str) and is_null_indicator(value, null_indicators):
            data[key] = None

def clean_year(year):
    if year and isinstance(year, str):
        if 'unknown' in year.lower():
            return None
        if '-' in year: # some languages have a range of years (e.g., '2023-2024')
            return year.split('-')[0]
        if not year.isdigit():
            print(f"Year '{year}' is not a number. Trying to extract year from string...")

            year_match = re.search(r"\d{4}", year) # cases like "2012(designed), 2014(published)" and "Category:2024:2024"
            if year_match:
                return year_match.group(0)
            else:
                print(f"Year not found in '{year}'. Setting to None.")
                return None
    return year

def search_for_year_category(language):
    if 'Categories' in language:
        categories = language['Categories']
        year_found = None
        for category in categories:
            if category.isdigit() and 1000 <= int(category) <= 9999:
                year_found = category
                break

        if year_found:
            print(f"Found year category: {year_found} in {language['LanguageName']}")
            language['YearCreated'] = year_found
            language['Categories'] = [cat for cat in categories if cat != year_found]

def extract_lang_name_from_url(url):
    try:
        path = urlparse(url).path
        if path:
            return unquote(path.split('/')[-1])
    except Exception:
        print(f"Error extracting language name from URL: {url}")
    return None

def clean_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for language in data:
        if str(language['LanguageName']) == 'nan': # Esolangs 'None' and 'NULL' names were converted to 'nan' in the JSON
            language['LanguageName'] = extract_lang_name_from_url(language['URL'])
            print(f"Extracted language name: {language['LanguageName']}")

        remove_null_indicators(language, ['unknown', 'none', 'n/a' , ''])

        if 'YearCreated' in language:
            language['YearCreated'] = clean_year(language['YearCreated'])

        if 'Categories' in language:
            search_for_year_category(language)

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data cleaned and saved to '{output_file}'.")

input_file = 'data/esolangs-data.json'
output_file = 'data/esolangs-cleaned.json'
clean_data(input_file, output_file)