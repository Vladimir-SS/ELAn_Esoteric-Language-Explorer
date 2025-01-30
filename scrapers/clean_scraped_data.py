import json
import re
from urllib.parse import urlparse, unquote

PARADIGMS = [
    "imperative", "functional", "string-rewriting", "object-oriented",
    "class-based", "prototype-based", "declarative",
    "particle-automata", "turning-tarpits", "self-modifying"
]

DIMENSIONS = [
    "zero-dimensional", "one-dimensional",
    "two-dimensional", "multi-dimensional",
]

MEMORY_SYSTEMS = [
    "cell-based", "stack-based", "queue-based",
    "deque-based", "tree-based", "matrix-based"
]

COMPUTATIONAL_CLASSES = [
    "turing-complete", "turing-tarpits", "linear-bounded-automata",
    "push-down-automata", "total", "uncomputable",
    "finite-state-automata"
]

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

def clean_array_fields(language, fields: list[str]):
    for field in fields:
        if language.get(field):
            language[field] = [value.lower().replace(" ", "-")  for value in language[field]]

def extract_year_from_categories(language):
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

def extract_attribute_from_categories(language, attribute, keywords):
    items = set(language.get(attribute) or [])
    new_categories = []

    for category in language["Categories"]:
        for keyword in keywords:
            if keyword in category:
                items.add(keyword)
                break
        else:
            new_categories.append(category)

    if items:
        language[attribute] = list(items)
    language["Categories"] = new_categories

def clean_categories(language):
    computational_classes = set(language.get("ComputationalClass") or [])
    categories = set(language.get("Categories") or [])

    common = computational_classes.intersection(categories)
    language["Categories"] = list(categories - common)

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

        clean_array_fields(language, ['Paradigms', 'Dimensions', 'MemorySystem', 'ComputationalClass', 'Categories'])

        if language.get('MemorySystem'):
            language['MemorySystem'] = [
                memory_system if "based" in memory_system.lower() else f"{memory_system}-based"
                for memory_system in language['MemorySystem']
            ] # Add '-based' to memory systems that don't have it

        if language.get('ComputationalClass'):
            language['ComputationalClass'] = [cc for cc in language['ComputationalClass'] if not cc.startswith('unknown')]

        extract_year_from_categories(language)
        extract_attribute_from_categories(language, "Paradigms", PARADIGMS)
        extract_attribute_from_categories(language, "Dimensions", DIMENSIONS)
        extract_attribute_from_categories(language, "MemorySystem", MEMORY_SYSTEMS)
        extract_attribute_from_categories(language, "ComputationalClass", COMPUTATIONAL_CLASSES)

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data cleaned and saved to '{output_file}'.")

input_file = 'data/esolangs-data.json'
output_file = 'data/esolangs-cleaned.json'
clean_data(input_file, output_file)
