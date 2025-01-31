import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import logging
from DataHandler import DataHandler

class EsolangScraper:
    BASE_URL = "https://esolangs.org"
    LANGUAGES_URL = f"{BASE_URL}/wiki/Language_list"

    def __init__(self, debug=False):
        self.data_dir = 'data'
        self.file_name = 'esolangs'
        os.makedirs(self.data_dir, exist_ok=True)

        self.links_file = os.path.join(self.data_dir, self.file_name + '-links.csv')
        self.output_file = os.path.join(self.data_dir, self.file_name + '-data.json')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

        self.data_handler = DataHandler()

        user_pattern = r"(User:\S+|[\w\s]+)"

        self.PATTERNS = {
            "Alias": [
                r"the title of this article is also called ([^.]+)",
                r"the correct title is actually ([^.]+)",
            ],
            "DesignedBy": [ # To do: Consider modifying patterns.
                rf"developed by {user_pattern}",
                rf"made by {user_pattern}",
                rf"invented by {user_pattern}",
                rf"implemented by {user_pattern}",
                rf"devised by {user_pattern}",
                rf"designed by {user_pattern}",
                rf"created by {user_pattern}",
                rf"discovered by {user_pattern}",
                r"by (User:\S+)", # This might find wrong results in particular cases
            ],
            "InfluencedBy": [
                r"inspired by (\S+)",
                r"clone of (\S+)",
                r"based on (\S+)", # Example of miss interpreted data: "Tree(3) is a language based on Chinese and Korean.", does not refer to an esolang in this case
            ],
            "YearCreated": [
                r"created in (\d{4})",
                r"in (\d{4})"
            ],
        }

        log_file = os.path.join(self.data_dir, 'esolang_scraper.log')

        logging_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=logging_level,
            format="%(asctime)s - %(levelname)s - %(message)s", # For additional info: %(filename)s:%(lineno)d
            handlers=[
                logging.FileHandler(log_file, mode='w', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        logging.info("Esolangs scraper initialized.")

    def load_html_content(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve html_content: {url}, due to {e}")
            return None

    def collect_links(self):
        html_content = self.load_html_content(self.LANGUAGES_URL)
        if not html_content:
            return []

        languages = html_content.find_all('li')
        language_links = []

        for lang in languages:
            a_tag = lang.find('a', href=True)
            if a_tag:
                language_name = a_tag.get('title', '').strip()

                if(language_name == "Esoteric programming language"):
                    break

                language_url = a_tag['href']
                logging.info(f"Found language: {language_name} - {language_url}")

                full_url = f"{self.BASE_URL}{language_url}"
                language_links.append([language_name, full_url])

        self.data_handler.save_to_csv(language_links, self.links_file, columns=["LanguageName", "URL"])
        logging.info(f"Scraped {len(language_links)} languages.")

    def load_languages_links(self):
        if not os.path.exists(self.links_file):
            self.collect_links()

        return pd.read_csv(self.links_file).iterrows()

    def extract_short_description(self, language_html_content):
        description = []
        current_element = language_html_content.find('p')

        while current_element:
            if current_element.name == 'div' or current_element.get('id') == 'toc':
                break  # Stop if we reach the Table of Contents div

            if current_element.name == 'p':
                description.append(current_element.get_text(strip=True))

            current_element = current_element.find_next_sibling()

        return ' '.join(description)

    def extract_extensions_from_html(self, cell):
        code_tags = cell.find_all('code')
        extensions = set()

        for tag in code_tags:
            text = tag.get_text()
            extensions.update(re.findall(r'\.\w+', text))

        return list(extensions)

    def extract_language_data_table(self, language_html_content):
        rename_mapping = {
            "Paradigm(s)": "Paradigms",
            "Designed by": "DesignedBy",
            "Appeared in": "YearCreated",
            "Memory system": "MemorySystem",
            "Dimensions": "Dimensions",  # No change
            "Computational class": "ComputationalClass",
            "Reference implementation": "ReferenceImplementation",
            "Influenced by": "InfluencedBy",
            "Influenced": "Influenced",  # No change
            "File extension(s)": "FileExtensions",
            "Dialects": "Dialects", # No change
            "Type system": "TypeSystem",
        }
        array_content_fields = ["Paradigm(s)", "Type system", "Dialects", "Influenced by", "Influenced", "Computational class", "Dimensions", "Memory system"]

        language_info = {new_key: None for new_key in rename_mapping.values()}

        table = language_html_content.find('table', style=lambda value: value and 'float:right' in value)

        if table:
            logging.info("Found data table")
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header:
                    matched_header = None
                    for key in rename_mapping.keys():
                        if key.lower() in header.text.strip().lower():  # Partial matching (case-insensitive)
                            matched_header = key
                            break

                    if matched_header:
                        cell = row.find('td')
                        if cell:
                            content = cell.get_text(strip=True)


                            if matched_header in array_content_fields:
                                if '<br/>' in str(cell) and matched_header in array_content_fields:
                                    logging.info(f"Found values separated by <br/> in {matched_header}")
                                    split_content = cell.decode_contents().split('<br/>')

                                    content = [BeautifulSoup(value.strip(), 'html.parser').get_text() for value in split_content] # Remove HTML tags for cases like <a href="...">...</a>
                                else:
                                    content = [value.strip() for value in content.split(',')]

                            if matched_header == "File extension(s)":
                                content = self.extract_extensions_from_html(cell)

                            language_info[rename_mapping[matched_header]] = content

        return language_info

    def extract_categories(self, language_html_content):
        catlinks = language_html_content.find('div', {'id': 'mw-normal-catlinks'})

        categories = []
        if catlinks:
            logging.info("Found categories")
            for li in catlinks.find_all('li'):
                category = li.text.strip()
                categories.append(category)

        return categories

    def scrape_languages(self, limit=None):
        languages_links = self.load_languages_links()
        languages_data = []

        for index, row in languages_links:
            if limit and index >= limit:
                break
            index += 1

            language_name = row['LanguageName']
            language_url = row['URL']
            logging.info(f"Scraping data for {language_name}...")

            html_content = self.load_html_content(language_url)
            if not html_content:
                continue

            language_info = self.extract_language_data_table(html_content)
            short_description = self.extract_short_description(html_content)
            categories = self.extract_categories(html_content)

            language_info["LanguageName"] = language_name
            language_info["URL"] = language_url
            language_info["ShortDescription"] = short_description
            language_info["Categories"] = categories

            self.fill_missing_fields(html_content, language_info)

            languages_data.append(language_info)
            # time.sleep(0.5)

        self.data_handler.save_to_json(languages_data, self.output_file)

    def extract_information(self, language_html_content, pattern_key):
        body_content = language_html_content.find(id="bodyContent")
        if body_content:
            text = body_content.get_text()
            for pattern in self.PATTERNS.get(pattern_key, []):
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()

        return None

    def fill_missing_fields(self, html_content, language_info):
        for field in self.PATTERNS.keys():  # Iterate over the keys of the language_info dictionary
            if language_info.get(field) is None:  # Check if the field is missing
                value = self.extract_information(html_content, field)
                if value:
                    logging.info(f"Found {field}: {value}")
                    language_info[field] = value

    def extract_wikitables_with_headers(self, language_html_content) -> list[dict[str, any]]:
        tables_with_headers = []
        all_tables = language_html_content.find_all('table', class_='wikitable')

        for table in all_tables:
            header_text = None
            for previous_sibling in table.find_previous_siblings():
                if previous_sibling.name in ['h2', 'h3', 'h4']:
                    span = previous_sibling.find('span', class_='mw-headline')
                    if span:
                        header_text = span.text.strip()
                        break

            rows = table.find_all('tr')
            table_headers = [th.get_text(strip=True) for th in rows[0].find_all('th')] if rows else []

            table_data = []
            for row in rows[1:]:  # Skip the header row
                cells = row.find_all(['td', 'th'])
                row_data = {table_headers[i]: cells[i].get_text(strip=True) if i < len(cells) else None
                            for i in range(len(table_headers))}
                table_data.append(row_data)

            tables_with_headers.append({
                "Header": header_text,
                "TableHeaders": table_headers,
                "Rows": table_data
            })

            logging.info(f"Extracted table: '{header_text}' with {len(table_data)} rows and columns: {table_headers}.")

        return tables_with_headers

    def check_for_tables(self, limit=None):
        languages_links = self.load_languages_links()
        tables_data = {}

        for index, row in languages_links:
            if limit and index >= limit:
                break
            index += 1

            language_name = row['LanguageName']
            logging.info(f"Scraping tables for {language_name}...")

            html_content = self.load_html_content(row['URL'])
            if not html_content:
                continue

            tables = self.extract_wikitables_with_headers(html_content)
            if tables:
                logging.info(f"Found {len(tables)} tables for {language_name}.")
                tables_data[language_name] = [
                    {
                        "Header": table["Header"],
                        "TableHeaders": table["TableHeaders"],
                        "Rows": table["Rows"],
                    }
                    for table in tables
                ]

        output_file = os.path.join(self.data_dir, "esolangs_tables.json")
        self.data_handler.save_to_json(tables_data, output_file)