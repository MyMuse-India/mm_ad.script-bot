from __future__ import annotations
import re
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger("mymuse")

@dataclass
class InstagramPost:
    post_id: str
    caption: str
    hashtags: List[str]
    likes_count: Optional[int]
    comments_count: Optional[int]
    post_type: str  # "image", "video", "carousel"
    timestamp: Optional[str]
    url: str

@dataclass
class InstagramProfile:
    username: str
    full_name: str
    bio: str
    followers_count: Optional[int]
    following_count: Optional[int]
    posts_count: Optional[int]
    posts: List[InstagramPost]


def _extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    if not text:
        return []
    hashtags = re.findall(r'#(\w+)', text)
    return [tag.lower() for tag in hashtags if len(tag) > 1]


def _extract_numbers(text: str) -> Optional[int]:
    """Extract first number from text."""
    if not text:
        return None
    match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)', text)
    if match:
        num_str = match.group(1).replace(',', '')
        try:
            return int(float(num_str))
        except ValueError:
            pass
    return None


def _clean_caption(text: str) -> str:
    """Clean Instagram caption text."""
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove @mentions
    text = re.sub(r'@\w+', '', text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove emojis (basic) - but keep some common ones
    text = re.sub(r'[^\w\s.,!?\'"\-()#]', '', text)
    
    # Clean up common Instagram artifacts
    text = re.sub(r'^\s*[•·]\s*', '', text)  # Remove bullet points
    text = re.sub(r'\s*[•·]\s*', ' ', text)  # Replace internal bullets with spaces
    
    # Remove common Instagram navigation text
    text = re.sub(r'\b(Follow|Follow us|Follow me|Follow for more)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(Click link in bio|Link in bio|Swipe|Tap)\b', '', text, flags=re.IGNORECASE)
    
    return text.strip()


def scrape_instagram_profile(username: str, max_posts: int = 50) -> Optional[InstagramProfile]:
    """
    Scrape Instagram profile data using Selenium.
    Returns InstagramProfile object or None if failed.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
    except ImportError:
        logger.error("Selenium not available. Install with: pip install selenium")
        return None

    profile_url = f"https://www.instagram.com/{username}/"
    posts: List[InstagramPost] = []
    
    driver = None
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        logger.info(f"Starting scrape of {profile_url}")
        driver.get(profile_url)
        
        # Wait for page to load
        time.sleep(8)
        
        # Log page title for debugging
        page_title = driver.title
        logger.info(f"Page title: {page_title}")
        
        # Extract profile info
        full_name = ""
        bio = ""
        followers = None
        following = None
        posts_count = None
        
        try:
            # Profile name - try multiple selectors
            name_selectors = [
                "h2",
                "h1",
                "[data-testid='user-bio'] + h2",
                "._aacl._aacs._aact._aacx._aada",
                "span[data-testid='user-bio'] + h2"
            ]
            
            for selector in name_selectors:
                try:
                    name_elem = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    full_name = name_elem.text.strip()
                    if full_name:
                        logger.info(f"Found profile name: {full_name}")
                        break
                except TimeoutException:
                    continue
            
            if not full_name:
                logger.warning("Could not find profile name")
                
        except Exception as e:
            logger.warning(f"Error finding profile name: {e}")
        
        try:
            # Bio - try multiple selectors
            bio_selectors = [
                "div[data-testid='user-bio']",
                "._aacl._aacs._aact._aacx._aada",
                ".-vDIg span",
                "[data-testid='user-bio']",
                "span[data-testid='user-bio']"
            ]
            
            for selector in bio_selectors:
                try:
                    bio_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    bio = bio_elem.text.strip()
                    if bio:
                        logger.info(f"Found bio: {bio[:100]}...")
                        break
                except NoSuchElementException:
                    continue
                    
            if not bio:
                logger.warning("Could not find bio")
                
        except Exception as e:
            logger.warning(f"Error finding bio: {e}")
        
        try:
            # Stats - try multiple approaches
            stats_selectors = [
                "li",
                "[data-testid='user-bio'] + ul li",
                "._aacl._aacs._aact._aacx._aada + ul li",
                "ul li"
            ]
            
            for selector in stats_selectors:
                try:
                    stats = driver.find_elements(By.CSS_SELECTOR, selector)
                    if stats:
                        for stat in stats:
                            text = stat.text.strip()
                            if 'posts' in text.lower():
                                posts_count = _extract_numbers(text)
                            elif 'followers' in text.lower():
                                followers = _extract_numbers(text)
                            elif 'following' in text.lower():
                                following = _extract_numbers(text)
                        if posts_count or followers or following:
                            logger.info(f"Found stats: posts={posts_count}, followers={followers}, following={following}")
                            break
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"Could not extract stats: {e}")
        
        # Try to find posts using multiple approaches
        posts_loaded = 0
        
        # First, try to find post containers
        post_selectors = [
            "article a[href*='/p/']",
            "a[href*='/p/']",
            "._aabd._aa8k._al3l a",
            "[data-testid='user-post'] a",
            "div[role='button'] a[href*='/p/']"
        ]
        
        post_elements = []
        for selector in post_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    post_elements = elements
                    logger.info(f"Found {len(elements)} posts using selector: {selector}")
                    break
            except Exception:
                continue
        
        if not post_elements:
            logger.warning("No post elements found with any selector")
            # Try scrolling to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Try again after scrolling
            for selector in post_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        post_elements = elements
                        logger.info(f"Found {len(elements)} posts after scrolling using selector: {selector}")
                        break
                except Exception:
                    continue
        
        # Process found posts
        for i, post_elem in enumerate(post_elements[:max_posts]):
            try:
                post_url = post_elem.get_attribute("href")
                if not post_url or "instagram.com/p/" not in post_url:
                    continue
                    
                # Extract post ID from URL
                post_id = post_url.split("/p/")[1].split("/")[0]
                
                # Try to get caption without opening modal (faster)
                caption = ""
                try:
                    # Look for caption in the post preview
                    caption_selectors = [
                        "._a9zr",
                        "._a9zs",
                        "[data-testid='post-caption']",
                        "._a9zr ._a9zs",
                        "div[data-testid='post-caption']"
                    ]
                    
                    for caption_selector in caption_selectors:
                        try:
                            caption_elem = post_elem.find_element(By.CSS_SELECTOR, caption_selector)
                            caption = caption_elem.text.strip()
                            if caption:
                                break
                        except NoSuchElementException:
                            continue
                            
                except Exception:
                    pass
                
                # If no caption found in preview, try opening the post
                if not caption:
                    try:
                        # Click on post to open modal
                        driver.execute_script("arguments[0].click();", post_elem)
                        time.sleep(2)
                        
                        # Extract caption from modal
                        modal_caption_selectors = [
                            "div[data-testid='post-caption']",
                            "._a9zs",
                            "._a9zr ._a9zs",
                            "span[data-testid='post-caption']"
                        ]
                        
                        for selector in modal_caption_selectors:
                            try:
                                caption_elem = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                )
                                caption = caption_elem.text.strip()
                                if caption:
                                    break
                            except TimeoutException:
                                continue
                        
                        # Close modal
                        try:
                            close_btn = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Close']")
                            close_btn.click()
                            time.sleep(1)
                        except NoSuchElementException:
                            # Try escape key
                            from selenium.webdriver.common.keys import Keys
                            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                            time.sleep(1)
                            
                    except Exception as e:
                        logger.warning(f"Error opening post modal: {e}")
                
                # Extract engagement (likes, comments)
                likes = None
                comments = None
                
                try:
                    # Look for engagement in post preview
                    engagement_selectors = [
                        "span:contains('like')",
                        "span:contains('comment')",
                        "[data-testid='like-count']",
                        "[data-testid='comment-count']"
                    ]
                    
                    for selector in engagement_selectors:
                        try:
                            elem = post_elem.find_element(By.CSS_SELECTOR, selector)
                            text = elem.text.strip()
                            if 'like' in text.lower():
                                likes = _extract_numbers(text)
                            elif 'comment' in text.lower():
                                comments = _extract_numbers(text)
                        except NoSuchElementException:
                            continue
                            
                except Exception:
                    pass
                
                # Determine post type
                post_type = "image"
                try:
                    video_elem = post_elem.find_element(By.CSS_SELECTOR, "video")
                    post_type = "video"
                except NoSuchElementException:
                    pass
                
                # Clean and create post object
                clean_caption = _clean_caption(caption)
                if clean_caption and len(clean_caption.strip()) > 5:  # Filter out very short captions
                    post = InstagramPost(
                        post_id=post_id,
                        caption=clean_caption,
                        hashtags=_extract_hashtags(caption),
                        likes_count=likes,
                        comments_count=comments,
                        post_type=post_type,
                        timestamp=None,  # Instagram doesn't show timestamps easily
                        url=post_url
                    )
                    posts.append(post)
                    posts_loaded += 1
                    logger.info(f"Scraped post {posts_loaded}: {post_id} - Caption length: {len(clean_caption)}")
                else:
                    logger.debug(f"Skipping post {post_id} - no valid caption")
            
            except Exception as e:
                logger.warning(f"Error processing post {i}: {e}")
                continue
        
        # If no posts found, try alternative approach
        if not posts:
            logger.info("No posts found with standard method, trying alternative method...")
            try:
                # Try to find any text content that might be captions
                text_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, p")
                potential_captions = []
                
                for elem in text_elements:
                    try:
                        text = elem.text.strip()
                        if text and len(text) > 20 and len(text) < 1000:  # Reasonable caption length
                            # Check if it looks like a caption (not navigation, not stats)
                            if not any(skip in text.lower() for skip in ['follow', 'posts', 'following', 'instagram', 'login', 'sign up']):
                                potential_captions.append(text)
                    except Exception:
                        continue
                
                if potential_captions:
                    logger.info(f"Found {len(potential_captions)} potential captions with alternative method")
                    # Create fake posts from these captions
                    for i, caption in enumerate(potential_captions[:max_posts]):
                        post = InstagramPost(
                            post_id=f"alt_{i}_{int(time.time())}",
                            caption=caption,
                            hashtags=_extract_hashtags(caption),
                            likes_count=None,
                            comments_count=None,
                            post_type="image",
                            timestamp=None,
                            url=f"https://www.instagram.com/{username}/"
                        )
                        posts.append(post)
                        posts_loaded += 1
                        logger.info(f"Created alternative post {posts_loaded} from caption: {caption[:50]}...")
                        
            except Exception as e:
                logger.warning(f"Alternative method also failed: {e}")
        
        # Create profile object
        profile = InstagramProfile(
            username=username,
            full_name=full_name,
            bio=bio,
            followers_count=followers,
            following_count=following,
            posts_count=posts_count,
            posts=posts
        )
        
        logger.info(f"Successfully scraped {len(posts)} posts from @{username}")
        return profile
        
    except Exception as e:
        logger.error(f"Failed to scrape Instagram profile @{username}: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def convert_to_training_data(profile: InstagramProfile, product_name: str = "mymuse") -> List[Dict[str, str]]:
    """Convert Instagram posts to training data format for the review index."""
    training_data = []
    
    for post in profile.posts:
        if post.caption and len(post.caption.strip()) > 10:  # Filter out very short captions
            training_data.append({
                "product_name": product_name,
                "text": post.caption,
                "source": f"instagram_{post.post_id}",
                "engagement": post.likes_count or 0,
                "hashtags": post.hashtags
            })
    
    return training_data


def save_training_data(training_data: List[Dict[str, str]], filename: str = "instagram_training_data.csv") -> str:
    """Save training data to CSV file."""
    import csv
    import os
    
    filepath = os.path.join("data", filename)
    os.makedirs("data", exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_name', 'text', 'source', 'engagement', 'hashtags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in training_data:
            # Convert hashtags list to string
            row_copy = row.copy()
            row_copy['hashtags'] = ','.join(row['hashtags'])
            writer.writerow(row_copy)
    
    logger.info(f"Saved {len(training_data)} training examples to {filepath}")
    return filepath


def scrape_and_train(username: str, product_name: str = "mymuse", max_posts: int = 50) -> Dict[str, Any]:
    """
    Main function: scrape Instagram profile and convert to training data.
    Returns summary of the operation.
    """
    logger.info(f"Starting Instagram scrape for @{username}")
    
    # Scrape profile
    profile = scrape_instagram_profile(username, max_posts)
    if not profile:
        return {"success": False, "error": "Failed to scrape profile"}
    
    # Convert to training data
    training_data = convert_to_training_data(profile, product_name)
    if not training_data:
        return {"success": False, "error": "No valid training data extracted"}
    
    # Save to CSV
    csv_path = save_training_data(training_data, f"instagram_{username}_{int(time.time())}.csv")
    
    return {
        "success": True,
        "username": username,
        "posts_scraped": len(profile.posts),
        "training_examples": len(training_data),
        "csv_path": csv_path,
        "profile_stats": {
            "followers": profile.followers_count,
            "following": profile.following_count,
            "total_posts": profile.posts_count
        }
    }
