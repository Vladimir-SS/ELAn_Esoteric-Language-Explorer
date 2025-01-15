import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os

class EsolangScraper:
    BASE_URL = "https://esolangs.org"
    LANGUAGES_URL = f"{BASE_URL}/wiki/Language_list"

    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)

        self.links_file = os.path.join(self.data_dir, 'esolangs_languages_links.csv')
        self.output_file = os.path.join(self.data_dir, 'esolangs_languages_data.json')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

    def save_links_to_csv(self, data):
        df = pd.DataFrame(data, columns=["Language Name", "URL"])
        df.to_csv(self.links_file, index=False, encoding='utf-8')
        print(f"Data saved to '{self.links_file}'.")

    def save_data_to_json(self, data):
        with open(self.output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data saved to '{self.output_file}'.")

    def load_html_content(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Failed to retrieve html_content: {url}, due to {e}")
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
                language_name = a_tag.get_text(strip=True)
                if(language_name == "Esoteric programming language"):
                    break

                language_url = a_tag['href']
                print(language_name, " ", language_url)

                full_url = f"{self.BASE_URL}{language_url}"
                language_links.append([language_name, full_url])

        self.save_links_to_csv(language_links)
        print(f"Scraped {len(language_links)} languages.")

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

    def extract_language_data_table(self, language_html_content):
        language_info = {
            "Paradigm(s)": None,
            "Designed by": None,
            "Appeared in": None,
            "Memory system": None,
            "Dimensions": None,
            "Computational class": None,
            "Reference implementation": None,
            "Influenced by": None,
            "File extension(s)": None
        }

        table = language_html_content.find('table', style=lambda value: value and 'float:right' in value)

        if table:
            print("Found data table")
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header and header.text.strip() in language_info:
                    cell = row.find('td')
                    if cell:
                        content = cell.get_text(strip=True)
                        if header.text.strip() in ["Paradigm(s)", "File extension(s)"]:
                            language_info[header.text.strip()] = [value.strip() for value in content.split(',')]
                        else:
                            language_info[header.text.strip()] = content
        return language_info

    def extract_categories(self, language_html_content):
        catlinks = language_html_content.find('div', {'id': 'mw-normal-catlinks'})

        categories = []
        if catlinks:
            print("Found categories")
            for li in catlinks.find_all('li'):
                category = li.text.strip()
                categories.append(category)

        return categories

    def scrape_languages(self):
        languages_links = self.load_languages_links()
        languages_data = []

        test_limit = 0 # Remove this to scrape all languages
        for index, row in languages_links:
            if test_limit == 20:
                break
            test_limit += 1

            language_name = row['Language Name']
            language_url = row['URL']
            print(f"Scraping data for {language_name}...")

            html_content = self.load_html_content(language_url)
            if not html_content:
                continue

            language_info = self.extract_language_data_table(html_content)
            short_description = self.extract_short_description(html_content)
            categories = self.extract_categories(html_content)

            language_info["Language Name"] = language_name
            language_info["URL"] = language_url
            language_info["Year created"] = language_info.pop("Appeared in")
            language_info["Paradigms"] = language_info.pop("Paradigm(s)")
            language_info["Short Description"] = short_description
            language_info["Categories"] = categories

            languages_data.append(language_info)
            time.sleep(1)

        self.save_data_to_json(languages_data)


scraper = EsolangScraper()
scraper.scrape_languages()