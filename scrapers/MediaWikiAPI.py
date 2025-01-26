import requests
import os
import logging
from urllib.parse import quote
import pandas as pd

class MediaWikiAPI:
    BASE_URL = "https://esolangs.org"
    MEDIA_WIKI_API = f"{BASE_URL}/w/api.php"

    def __init__(self, debug=False):
        self.data_dir = "data"
        self.file_name = "media_wiki_esolang"
        os.makedirs(self.data_dir, exist_ok=True)

        self.links_file = os.path.join(self.data_dir, self.file_name + '-links.csv')

        logging_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

    def collect_languages(self):
        languages = []
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Languages",
            "cmlimit": "500",
            "format": "json"
        }

        while True:
            logging.info("Requesting data from MediaWiki API...")
            response = requests.get(self.MEDIA_WIKI_API, params=params)
            response.raise_for_status()
            data = response.json()

            for member in data['query']['categorymembers']:
                title = member['title']

                if title.startswith("Category:"):
                    logging.debug(f"Skipping category: {title}")
                    continue

                url = f"{self.BASE_URL}/wiki/{quote(title)}"

                languages.append([title, url])
                logging.debug(f"Collected: {title} -> {url}")

            if 'continue' in data:
                params['cmcontinue'] = data['continue']['cmcontinue']
                logging.info("Continuing to next batch...")
            else:
                break

        return languages

    def fetch_all_categories(self):
        categories = []
        params = {
            "action": "query",
            "list": "allcategories",
            "aclimit": "500",
            "format": "json"
        }

        while True:
            response = requests.get(self.MEDIA_WIKI_API, params=params)
            data = response.json()

            categories.extend([cat['*'] for cat in data['query']['allcategories']])

            if 'continue' in data:
                params['accontinue'] = data['continue']['accontinue']
            else:
                break

        self.categories = categories
        logging.info(f"Fetched {len(categories)} categories.")
        return categories

    def fetch_languages_by_category(self, category):
        """
        Fetches the languages from a specific category.
        """
        languages = []
        category = "Category:" + category.replace(" ", "_")

        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": "500",
            "format": "json"
        }

        while True:
            response = requests.get(self.MEDIA_WIKI_API, params=params)
            data = response.json()

            languages.extend([member['title'] for member in data['query']['categorymembers']])

            if 'continue' in data:
                params['cmcontinue'] = data['continue']['cmcontinue']
            else:
                break

        logging.info(f"Fetched {len(languages)} languages under {category}.")
        return languages


    def save_links_to_csv(self, data):
        """
        Save the list of languages and URLs to a CSV file.
        """
        df = pd.DataFrame(data, columns=["LanguageName", "URL"])
        df.to_csv(self.links_file, index=False, encoding='utf-8')
        logging.info(f"Data saved to '{self.links_file}'.")

if __name__ == "__main__":
    media_wiki = MediaWikiAPI(debug=True)

    # languages = media_wiki.collect_languages()
    # media_wiki.save_links_to_csv(languages)
    # logging.info(f"Collected {len(languages)} languages.")

    categories = media_wiki.fetch_all_categories()
    logging.info(f"Found {len(categories)} categories.")

    for category in categories:
        languages = media_wiki.fetch_languages_by_category(category)
        logging.info(f"Found {len(languages)} languages in {category}.")