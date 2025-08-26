# instagram_scraper.py — Instagram content extraction for MyMuse training data
from __future__ import annotations
import os, csv, tempfile, logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("mymuse")

def scrape_instagram_posts(username: str, product_name: str, max_posts: int = 50) -> Dict:
    """
    Scrape Instagram posts from @mymuse.in and convert to training data.
    Returns dict with success status, CSV path, and training examples count.
    """
    try:
        # Import selenium components
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.common.exceptions import TimeoutException, WebDriverException
    except ImportError:
        logger.warning("Selenium not available for Instagram scraping")
        return {
            "success": False,
            "error": "Selenium not available",
            "csv_path": None,
            "training_examples": 0
        }
    
    try:
        # Set up Chrome options for headless scraping
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        try:
            # Navigate to Instagram profile
            profile_url = f"https://www.instagram.com/{username}/"
            logger.info(f"Scraping Instagram profile: {profile_url}")
            driver.get(profile_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract post content
            posts_data = []
            
            # Look for post elements (Instagram's structure may vary)
            post_selectors = [
                "article a[href*='/p/']",
                "div[data-testid='post']",
                "div[class*='post']",
                "article div[class*='caption']"
            ]
            
            posts_found = 0
            for selector in post_selectors:
                try:
                    post_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if post_elements:
                        logger.info(f"Found {len(post_elements)} posts using selector: {selector}")
                        break
                except Exception:
                    continue
            
            # Extract text from posts
            for i, post in enumerate(post_elements[:max_posts]):
                try:
                    # Try to get post text/caption
                    caption_selectors = [
                        "div[class*='caption']",
                        "div[class*='text']",
                        "span[class*='caption']",
                        "div[class*='content']"
                    ]
                    
                    post_text = ""
                    for caption_selector in caption_selectors:
                        try:
                            caption_elem = post.find_element(By.CSS_SELECTOR, caption_selector)
                            post_text = caption_elem.text.strip()
                            if post_text:
                                break
                        except Exception:
                            continue
                    
                    if post_text:
                        posts_data.append({
                            "product_name": product_name,
                            "text": post_text,
                            "source": "instagram",
                            "username": username,
                            "scraped_at": datetime.now().isoformat()
                        })
                        posts_found += 1
                        
                except Exception as e:
                    logger.warning(f"Error extracting post {i}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {posts_found} posts from Instagram")
            
            # Save to CSV
            if posts_data:
                timestamp = int(datetime.now().timestamp())
                csv_filename = f"mymuse_instagram_{username}_{timestamp}.csv"
                csv_path = os.path.join("data", csv_filename)
                
                # Ensure data directory exists
                os.makedirs("data", exist_ok=True)
                
                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ["product_name", "text", "source", "username", "scraped_at"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(posts_data)
                
                logger.info(f"Saved {len(posts_data)} Instagram posts to {csv_path}")
                
                return {
                    "success": True,
                    "csv_path": csv_path,
                    "training_examples": len(posts_data),
                    "username": username,
                    "message": f"Successfully scraped {len(posts_data)} posts from @{username}"
                }
            else:
                return {
                    "success": False,
                    "error": "No posts found",
                    "csv_path": None,
                    "training_examples": 0
                }
                
        finally:
            driver.quit()
            
    except TimeoutException:
        logger.error("Timeout while scraping Instagram")
        return {
            "success": False,
            "error": "Timeout while loading Instagram page",
            "csv_path": None,
            "training_examples": 0
        }
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        return {
            "success": False,
            "error": f"WebDriver error: {str(e)}",
            "csv_path": None,
            "training_examples": 0
        }
    except Exception as e:
        logger.error(f"Unexpected error in Instagram scraping: {e}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "csv_path": None,
            "training_examples": 0
        }

if __name__ == "__main__":
    # Test the scraper
    result = scrape_instagram_posts("mymuse.in", "mymuse", 20)
    print(f"Scraping result: {result}")
