# -*- coding: utf-8 -*-
"""
Created on 8.08.2024

@author: Dannya Chami
"""


import requests
from bs4 import BeautifulSoup


class GoogleSearch:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def search(self, query):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'lr': 'lang_tr',  # Language restriction to Turkish
            'cr': 'countryTR'  # Country restriction to Turkey
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


class ContentFetcher:
    @staticmethod
    def is_valid_paragraph(text, min_words=15):
        words = len(text.split())
        return words >= min_words

    @staticmethod
    def fetch_page_content(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    page_soup = BeautifulSoup(response.text, 'html.parser')
                    paragraphs = page_soup.find_all('p')

                    valid_paragraphs = [p.text for p in paragraphs if ContentFetcher.is_valid_paragraph(p.text)]

                    if len(valid_paragraphs) >= 3:
                        content = "\n".join(valid_paragraphs[:4])
                        return content.strip()
                    else:
                        return "Yeterli sayida gecerli paragraf yok"
                else:
                    return "Icerik HTML formatinda degildir"
            else:
                return "Sayfa getirilemedi"
        except Exception as e:
            return f"Error fetching the page: {e}"


class TextSearcher:
    def __init__(self, api_key, search_engine_id):
        self.google_search = GoogleSearch(api_key, search_engine_id)
        self.content_fetcher = ContentFetcher()

    def search_show_text(self, query):
        results = self.google_search.search(query)

        if "error" in results:
            pass
            # print(f"An error occurred: {results['error']}")

        elif 'items' in results:
            for i, item in enumerate(results['items']):
                link = item['link']
                content = self.content_fetcher.fetch_page_content(link)

                if any(content.startswith(error) for error in [
                    "Error", "Icerik HTML formatinda degildir", 
                    "Sayfa getirilemedi", "Yeterli sayida gecerli paragraf yok"
                ]):
                    continue
                else:
                    words = content.split()
                    if len(words) >= 30:
                        subject = query.replace(" nedir", "")
                        print(f"'{subject}' hakkinda icerik:\n{content}\n")
                        break
        else:
            print("Hic bir sonuc bulunamamistir.")
