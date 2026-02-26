"""
Web Scraper Tool for Open Interpreter
Intelligent web scraping with templates and anti-bot detection
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ScraperTool:
    """Intelligent web scraper with templates"""

    def __init__(self):
        self.driver = None
        self.wait_time = 10
        self.rate_limit_delay = 2  # seconds between requests

    def _init_driver(self, headless: bool = True):
        """Initialize Selenium WebDriver"""
        if self.driver:
            return

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Anti-bot detection
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    async def scrape(
        self,
        url: str,
        template: str = "auto",
        max_pages: int = 1,
        export_format: str = "json",
    ) -> Dict[str, Any]:
        """
        Scrape a website using templates

        Args:
            url: URL to scrape
            template: Template to use (auto, youtube, ecommerce, news, linkedin, github, custom)
            max_pages: Maximum pages to scrape (for pagination)
            export_format: Export format (json, csv, excel)

        Returns:
            Scraped data
        """
        self._init_driver()

        try:
            # Auto-detect template if needed
            if template == "auto":
                template = self._detect_template(url)

            # Select scraping method based on template
            if template == "youtube":
                data = await self._scrape_youtube(url, max_pages)
            elif template == "ecommerce":
                data = await self._scrape_ecommerce(url, max_pages)
            elif template == "news":
                data = await self._scrape_news(url, max_pages)
            elif template == "linkedin":
                data = await self._scrape_linkedin(url, max_pages)
            elif template == "github":
                data = await self._scrape_github(url, max_pages)
            else:
                data = await self._scrape_generic(url, max_pages)

            # Export data
            exported = self._export_data(data, export_format)

            return {
                "success": True,
                "template": template,
                "url": url,
                "pages_scraped": len(data.get("items", [])),
                "data": data,
                "exported": exported,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "url": url}

        finally:
            self._close_driver()

    def _detect_template(self, url: str) -> str:
        """Auto-detect scraping template based on URL"""
        domain = urlparse(url).netloc.lower()

        if "youtube.com" in domain or "youtu.be" in domain:
            return "youtube"
        elif "amazon.com" in domain or "ebay.com" in domain or "shopify" in domain:
            return "ecommerce"
        elif "linkedin.com" in domain:
            return "linkedin"
        elif "github.com" in domain:
            return "github"
        elif any(
            news in domain
            for news in ["news", "cnn", "bbc", "nytimes", "reddit", "hackernews"]
        ):
            return "news"
        else:
            return "generic"

    async def _scrape_youtube(
        self, url: str, max_pages: int
    ) -> Dict[str, Any]:
        """Scrape YouTube videos/channels"""
        self.driver.get(url)
        await asyncio.sleep(self.rate_limit_delay)

        # Wait for content to load
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.ID, "content"))
        )

        # Scroll to load more videos
        for _ in range(max_pages):
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            await asyncio.sleep(2)

        # Extract video data
        videos = []
        video_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer, ytd-grid-video-renderer")

        for elem in video_elements:
            try:
                title = elem.find_element(By.ID, "video-title").text
                link = elem.find_element(By.ID, "video-title").get_attribute("href")
                channel = elem.find_element(By.CSS_SELECTOR, "#channel-name a").text
                views = elem.find_element(By.CSS_SELECTOR, "#metadata-line span:first-child").text
                uploaded = elem.find_element(By.CSS_SELECTOR, "#metadata-line span:last-child").text

                videos.append({
                    "title": title,
                    "url": link,
                    "channel": channel,
                    "views": views,
                    "uploaded": uploaded,
                })
            except Exception:
                continue

        return {"type": "youtube", "items": videos}

    async def _scrape_ecommerce(
        self, url: str, max_pages: int
    ) -> Dict[str, Any]:
        """Scrape e-commerce product listings"""
        self.driver.get(url)
        await asyncio.sleep(self.rate_limit_delay)

        products = []

        for page in range(max_pages):
            # Wait for products to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result'], .product-item, .product-card"))
            )

            # Extract product data
            product_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "[data-component-type='s-search-result'], .product-item, .product-card"
            )

            for elem in product_elements:
                try:
                    title = elem.find_element(By.CSS_SELECTOR, "h2, .product-title, .product-name").text
                    price = elem.find_element(By.CSS_SELECTOR, ".a-price-whole, .price, .product-price").text
                    link = elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    products.append({"title": title, "price": price, "url": link})
                except Exception:
                    continue

            # Navigate to next page
            if page < max_pages - 1:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, ".s-pagination-next, .next, .pagination-next")
                    next_button.click()
                    await asyncio.sleep(self.rate_limit_delay)
                except Exception:
                    break

        return {"type": "ecommerce", "items": products}

    async def _scrape_news(self, url: str, max_pages: int) -> Dict[str, Any]:
        """Scrape news articles"""
        self.driver.get(url)
        await asyncio.sleep(self.rate_limit_delay)

        articles = []

        # Wait for articles to load
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article, .post, .story, .athing"))
        )

        # Extract article data
        article_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "article, .post, .story, .athing"
        )

        for elem in article_elements:
            try:
                title = elem.find_element(By.CSS_SELECTOR, "h1, h2, h3, .title, .storylink").text
                link = elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                articles.append({"title": title, "url": link})
            except Exception:
                continue

        return {"type": "news", "items": articles}

    async def _scrape_linkedin(
        self, url: str, max_pages: int
    ) -> Dict[str, Any]:
        """Scrape LinkedIn profiles/jobs"""
        # Note: LinkedIn requires authentication
        return {
            "type": "linkedin",
            "items": [],
            "note": "LinkedIn scraping requires authentication. Please log in manually.",
        }

    async def _scrape_github(self, url: str, max_pages: int) -> Dict[str, Any]:
        """Scrape GitHub repositories"""
        self.driver.get(url)
        await asyncio.sleep(self.rate_limit_delay)

        repos = []

        # Wait for repos to load
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article, .repo-list-item"))
        )

        # Extract repo data
        repo_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "article, .repo-list-item"
        )

        for elem in repo_elements:
            try:
                name = elem.find_element(By.CSS_SELECTOR, "h3 a, .repo-name a").text
                link = elem.find_element(By.CSS_SELECTOR, "h3 a, .repo-name a").get_attribute("href")
                description = elem.find_element(By.CSS_SELECTOR, "p, .repo-description").text

                repos.append({"name": name, "url": link, "description": description})
            except Exception:
                continue

        return {"type": "github", "items": repos}

    async def _scrape_generic(self, url: str, max_pages: int) -> Dict[str, Any]:
        """Generic scraping for any website"""
        self.driver.get(url)
        await asyncio.sleep(self.rate_limit_delay)

        # Extract all links and text
        links = []
        link_elements = self.driver.find_elements(By.TAG_NAME, "a")

        for elem in link_elements:
            try:
                text = elem.text.strip()
                href = elem.get_attribute("href")
                if text and href:
                    links.append({"text": text, "url": href})
            except Exception:
                continue

        # Extract page title
        title = self.driver.title

        return {"type": "generic", "title": title, "items": links}

    def _export_data(self, data: Dict[str, Any], format: str) -> str:
        """Export scraped data to specified format"""
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "csv":
            # TODO: Implement CSV export
            return "CSV export not implemented yet"
        elif format == "excel":
            # TODO: Implement Excel export
            return "Excel export not implemented yet"
        else:
            return json.dumps(data, indent=2)

    async def scrape_channel(self, channel_url: str) -> Dict[str, Any]:
        """Scrape YouTube channel for AI training datasets"""
        return await self.scrape(channel_url, template="youtube", max_pages=10)

    async def scrape_list(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Batch scraping with parallel processing"""
        results = []
        for url in urls:
            result = await self.scrape(url)
            results.append(result)
            await asyncio.sleep(self.rate_limit_delay)
        return results
