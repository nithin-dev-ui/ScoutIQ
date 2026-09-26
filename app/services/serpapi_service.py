import os

from dotenv import load_dotenv
import serpapi


load_dotenv()


class SerpApiService:
    def __init__(self):
        api_key = os.getenv("SERPAPI_KEY")

        if not api_key or api_key == "YOUR_KEY_HERE":
            raise ValueError("SERPAPI_KEY is missing from .env")

        self.client = serpapi.Client(api_key=api_key)

    def google_search(self, query, location="India"):
        return self.client.search({
            "engine": "google",
            "q": query,
            "location": location
        })

    def google_news_search(self, query):
        return self.client.search({
            "engine": "google_news",
            "q": query,
            "gl": "in",
            "hl": "en"
        })

    def google_scholar_search(self, query):
        return self.client.search({
            "engine": "google_scholar",
            "q": query,
            "hl": "en"
        })

    def google_jobs_search(self, query, location="India"):
        return self.client.search({
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "gl": "in",
            "hl": "en"
        })