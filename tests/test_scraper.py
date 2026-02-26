"""
Tests for web scraper module
"""

import asyncio
import pytest
from interpreter.tools.scraper import ScraperTool


@pytest.mark.asyncio
async def test_scraper_init():
    """Test scraper initialization"""
    scraper = ScraperTool()
    assert scraper.driver is None
    assert scraper.wait_time == 10
    assert scraper.rate_limit_delay == 2


@pytest.mark.asyncio
async def test_template_detection():
    """Test auto-detection of scraping templates"""
    scraper = ScraperTool()
    
    assert scraper._detect_template("https://youtube.com/watch?v=123") == "youtube"
    assert scraper._detect_template("https://amazon.com/product/123") == "ecommerce"
    assert scraper._detect_template("https://linkedin.com/in/user") == "linkedin"
    assert scraper._detect_template("https://github.com/user/repo") == "github"
    assert scraper._detect_template("https://news.ycombinator.com") == "news"
    assert scraper._detect_template("https://example.com") == "generic"


@pytest.mark.asyncio
async def test_scraper_config():
    """Test scraper configuration"""
    scraper = ScraperTool()
    scraper.wait_time = 15
    scraper.rate_limit_delay = 3
    
    assert scraper.wait_time == 15
    assert scraper.rate_limit_delay == 3


def test_export_json():
    """Test JSON export"""
    scraper = ScraperTool()
    data = {"type": "test", "items": [{"title": "Test", "url": "https://example.com"}]}
    
    exported = scraper._export_data(data, "json")
    assert "test" in exported
    assert "Test" in exported


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
