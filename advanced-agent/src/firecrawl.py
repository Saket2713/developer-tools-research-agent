import os
import time
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def search_companies(self, query: str, num_results: int = 5):
        """Search for companies with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                result = self.app.search(
                    query=f"{query} company pricing",
                    limit=num_results,
                    scrape_options=ScrapeOptions(
                        formats=["markdown"]
                    )
                )
                return result
            except Exception as e:
                error_str = str(e).lower()
                if attempt < self.max_retries - 1:
                    if "502" in error_str or "503" in error_str or "timeout" in error_str:
                        print(f"⚠️ Firecrawl server error (attempt {attempt + 1}/{self.max_retries}), retrying in {self.retry_delay}s...")
                        time.sleep(self.retry_delay)
                        continue
                    elif "rate" in error_str or "429" in error_str:
                        print(f"⚠️ Firecrawl rate limit (attempt {attempt + 1}/{self.max_retries}), waiting {self.retry_delay * 2}s...")
                        time.sleep(self.retry_delay * 2)
                        continue

                print(f"❌ Firecrawl search failed: {e}")
                return []

    def scrape_company_pages(self, url: str):
        """Scrape company pages with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                result = self.app.scrape_url(
                    url,
                    formats=["markdown"]
                )
                return result
            except Exception as e:
                error_str = str(e).lower()
                if attempt < self.max_retries - 1:
                    if "502" in error_str or "503" in error_str or "timeout" in error_str:
                        print(f"⚠️ Firecrawl server error scraping {url} (attempt {attempt + 1}/{self.max_retries}), retrying in {self.retry_delay}s...")
                        time.sleep(self.retry_delay)
                        continue
                    elif "rate" in error_str or "429" in error_str:
                        print(f"⚠️ Firecrawl rate limit scraping {url} (attempt {attempt + 1}/{self.max_retries}), waiting {self.retry_delay * 2}s...")
                        time.sleep(self.retry_delay * 2)
                        continue

                print(f"❌ Firecrawl scrape failed for {url}: {e}")
                return None

