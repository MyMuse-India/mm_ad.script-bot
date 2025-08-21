from __future__ import annotations
import re
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Import Selenium components at the top level
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Warning: Selenium not available. Install with: pip install selenium")

logger = logging.getLogger("mymuse")

@dataclass
class MyMuseProduct:
    name: str
    description: str
    price: str
    original_price: str
    discount: str
    rating: str
    reviews_count: str
    category: str
    features: List[str]
    url: str

@dataclass
class MyMuseReview:
    author: str
    rating: str
    text: str
    product: str

@dataclass
class MyMuseWebsiteData:
    products: List[MyMuseProduct]
    reviews: List[MyMuseReview]
    categories: List[str]
    testimonials: List[str]
    total_items: int


def _handle_age_verification(driver):
    """Handle the 21+ age verification popup."""
    try:
        # Look for the age verification button
        age_selectors = [
            "button:contains('Yes, I'm 21+')",
            "button:contains('Yes')",
            "button:contains('21+')",
            "[data-testid='age-verification-yes']",
            ".age-verification button",
            "button[class*='age']"
        ]
        
        for selector in age_selectors:
            try:
                # Try to find button by text content
                buttons = driver.find_elements("tag name", "button")
                for button in buttons:
                    button_text = button.text.strip().lower()
                    if any(age_text in button_text for age_text in ['yes', '21+', '21', 'older']):
                        logger.info("Found age verification button, clicking...")
                        button.click()
                        time.sleep(2)
                        return True
            except Exception:
                continue
        
        # Alternative: try to find by common patterns
        try:
            # Look for any button that might be age verification
            all_buttons = driver.find_elements("tag name", "button")
            for button in all_buttons:
                try:
                    text = button.text.strip()
                    if len(text) < 20 and any(word in text.lower() for word in ['yes', '21', 'older', 'continue']):
                        logger.info(f"Trying age verification button: {text}")
                        button.click()
                        time.sleep(2)
                        return True
                except Exception:
                    continue
        except Exception:
            pass
        
        logger.warning("Could not find age verification button, continuing anyway...")
        return False
        
    except Exception as e:
        logger.warning(f"Error handling age verification: {e}")
        return False


def scrape_mymuse_website(url: str = "https://mymuse.in/collections/deal-of-the-day") -> Optional[MyMuseWebsiteData]:
    """
    Scrape MyMuse website data including products, reviews, and testimonials.
    Returns MyMuseWebsiteData object or None if failed.
    """
    if not SELENIUM_AVAILABLE:
        return None

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
        logger.info(f"Starting scrape of {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Handle age verification
        _handle_age_verification(driver)
        
        # Wait a bit more for page to fully load
        time.sleep(3)
        
        # Log page title for debugging
        page_title = driver.title
        logger.info(f"Page title: {page_title}")
        
        # Extract products
        products = _extract_products(driver)
        logger.info(f"Found {len(products)} products")
        
        # Extract reviews
        reviews = _extract_reviews(driver)
        logger.info(f"Found {len(reviews)} reviews")
        
        # Extract categories
        categories = _extract_categories(driver)
        logger.info(f"Found {len(categories)} categories")
        
        # Extract testimonials
        testimonials = _extract_testimonials(driver)
        logger.info(f"Found {len(testimonials)} testimonials")
        
        # Create website data object
        website_data = MyMuseWebsiteData(
            products=products,
            reviews=reviews,
            categories=categories,
            testimonials=testimonials,
            total_items=len(products) + len(reviews) + len(testimonials)
        )
        
        logger.info(f"Successfully scraped MyMuse website: {website_data.total_items} total items")
        return website_data
        
    except Exception as e:
        logger.error(f"Failed to scrape MyMuse website: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def _extract_products(driver) -> List[MyMuseProduct]:
    """Extract product information from the page."""
    products = []
    elements = []  # Initialize elements variable
    
    try:
        # Look for product containers
        product_selectors = [
            "div[class*='product']",
            "div[class*='card']",
            "article",
            "[data-testid='product']",
            ".product-item"
        ]
        
        for selector in product_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(f"Found {len(elements)} product elements using selector: {selector}")
                    break
            except Exception:
                continue
        
        # If no specific product containers found, try to find any product-like content
        if not elements:
            # Look for text that might be product descriptions
            text_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, p, h1, h2, h3, h4, h5, h6")
            potential_products = []
            
            for elem in text_elements:
                try:
                    text = elem.text.strip()
                    if text and len(text) > 20 and len(text) < 500:
                        # Check if it looks like product content
                        if any(keyword in text.lower() for keyword in ['massager', 'vibrator', 'lubricant', 'toy', 'pleasure', 'intimate', 'groove', 'pulse', 'dive', 'edge', 'breeze']):
                            potential_products.append(text)
                except Exception:
                    continue
            
            # If still no products, try to get any meaningful text
            if not potential_products:
                logger.info("No specific product content found, trying general text extraction...")
                for elem in text_elements:
                    try:
                        text = elem.text.strip()
                        if text and len(text) > 30 and len(text) < 300:
                            # Avoid navigation and common page elements
                            skip_words = ['follow', 'login', 'sign up', 'cart', 'search', 'menu', 'navigation', 'instagram', 'facebook', 'twitter']
                            if not any(skip in text.lower() for skip in skip_words):
                                potential_products.append(text)
                    except Exception:
                        continue
            
            # If still no products, try to get page source and extract text manually
            if not potential_products:
                logger.info("Trying page source text extraction...")
                try:
                    page_source = driver.page_source
                    # Look for common MyMuse product patterns
                    import re
                    product_patterns = [
                        r'Groove\+.*?App-Enabled Wand.*?Flexible, ribbed wand for targeted internal and external pleasure',
                        r'Edge.*?Vibrating Stroker.*?The ultimate men\'s stroker',
                        r'Dive.*?Remote Controlled Massager.*?A remote-controlled egg massager',
                        r'Pulse.*?Targeted Massager.*?A sleek, discreet full-body massager',
                        r'Breeze.*?mini massager.*?playful sensations'
                    ]
                    
                    for pattern in product_patterns:
                        matches = re.findall(pattern, page_source, re.DOTALL | re.IGNORECASE)
                        for match in matches:
                            if match and len(match.strip()) > 20:
                                potential_products.append(match.strip())
                except Exception as e:
                    logger.warning(f"Page source extraction failed: {e}")
            
            # Create fake products from found text
            for i, text in enumerate(potential_products[:10]):  # Limit to 10
                product = MyMuseProduct(
                    name=f"Product_{i+1}",
                    description=text,
                    price="",
                    original_price="",
                    discount="",
                    rating="",
                    reviews_count="",
                    category="",
                    features=[],
                    url=""
                )
                products.append(product)
            
            return products
        
        # Process found product elements
        for i, elem in enumerate(elements[:20]):  # Limit to 20 products
            try:
                # Extract product name
                name = ""
                name_selectors = ["h1", "h2", "h3", "h4", "h5", "h6", "[class*='title']", "[class*='name']"]
                for selector in name_selectors:
                    try:
                        name_elem = elem.find_element(By.CSS_SELECTOR, selector)
                        name = name_elem.text.strip()
                        if name:
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract description
                description = ""
                desc_selectors = ["p", "span", "div[class*='description']", "div[class*='desc']"]
                for selector in desc_selectors:
                    try:
                        desc_elem = elem.find_element(By.CSS_SELECTOR, selector)
                        description = desc_elem.text.strip()
                        if description and len(description) > 10:
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract price information
                price = ""
                original_price = ""
                discount = ""
                
                try:
                    price_elements = elem.find_elements(By.CSS_SELECTOR, "span, div")
                    for price_elem in price_elements:
                        text = price_elem.text.strip()
                        if '₹' in text:
                            if '~~' in text:  # Original price
                                original_price = text
                            else:  # Current price
                                price = text
                        elif '%' in text and 'off' in text.lower():  # Discount
                            discount = text
                except Exception:
                    pass
                
                # Extract rating and reviews
                rating = ""
                reviews_count = ""
                
                try:
                    rating_elements = elem.find_elements(By.CSS_SELECTOR, "span, div")
                    for rating_elem in rating_elements:
                        text = rating_elem.text.strip()
                        if re.search(r'\d+\.\d+', text):  # Rating like 4.7
                            rating = text
                        elif 'review' in text.lower():  # Review count
                            reviews_count = text
                except Exception:
                    pass
                
                # Extract category
                category = ""
                try:
                    # Look for category indicators in the text
                    if any(word in description.lower() for word in ['women', 'her']):
                        category = "For Her"
                    elif any(word in description.lower() for word in ['men', 'him']):
                        category = "For Him"
                    elif any(word in description.lower() for word in ['couple', 'couples']):
                        category = "For Couples"
                except Exception:
                    pass
                
                # Extract features
                features = []
                try:
                    feature_elements = elem.find_elements(By.CSS_SELECTOR, "li, span, div")
                    for feature_elem in feature_elements:
                        text = feature_elem.text.strip()
                        if text and len(text) > 5 and len(text) < 100:
                            if any(keyword in text.lower() for keyword in ['vibration', 'remote', 'app', 'waterproof', 'silent', 'powerful']):
                                features.append(text)
                except Exception:
                    pass
                
                # Create product object if we have meaningful data
                if name or description:
                    product = MyMuseProduct(
                        name=name or f"Product_{i+1}",
                        description=description,
                        price=price,
                        original_price=original_price,
                        discount=discount,
                        rating=rating,
                        reviews_count=reviews_count,
                        category=category,
                        features=features,
                        url=""
                    )
                    products.append(product)
                    logger.info(f"Extracted product: {name or f'Product_{i+1}'}")
            
            except Exception as e:
                logger.warning(f"Error processing product {i}: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error extracting products: {e}")
    
    return products


def _extract_reviews(driver) -> List[MyMuseReview]:
    """Extract customer reviews from the page."""
    reviews = []
    elements = []  # Initialize elements variable
    
    try:
        # Look for review containers
        review_selectors = [
            "div[class*='review']",
            "div[class*='testimonial']",
            "[data-testid='review']",
            ".review-item"
        ]
        
        for selector in review_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(f"Found {len(elements)} review elements using selector: {selector}")
                    break
            except Exception:
                continue
        
        # If no specific review containers found, try to find review-like text
        if not elements:
            text_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, p")
            potential_reviews = []
            
            for elem in text_elements:
                try:
                    text = elem.text.strip()
                    if text and len(text) > 30 and len(text) < 300:
                        # Check if it looks like a review
                        if any(keyword in text.lower() for keyword in ['love', 'great', 'amazing', 'perfect', 'recommend', 'happy', 'satisfied']):
                            potential_reviews.append(text)
                except Exception:
                    continue
            
            # Create fake reviews from found text
            for i, text in enumerate(potential_reviews[:10]):  # Limit to 10
                review = MyMuseReview(
                    author=f"Customer_{i+1}",
                    rating="5.0",
                    text=text,
                    product="MyMuse Product"
                )
                reviews.append(review)
            
            return reviews
        
        # Process found review elements
        for i, elem in enumerate(elements[:15]):  # Limit to 15 reviews
            try:
                # Extract review text
                text = ""
                text_selectors = ["p", "span", "div[class*='text']", "div[class*='content']"]
                for selector in text_selectors:
                    try:
                        text_elem = elem.find_element(By.CSS_SELECTOR, selector)
                        text = text_elem.text.strip()
                        if text and len(text) > 10:
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract author
                author = ""
                author_selectors = ["span[class*='author']", "div[class*='author']", "strong", "b"]
                for selector in author_selectors:
                    try:
                        author_elem = elem.find_element(By.CSS_SELECTOR, selector)
                        author = author_elem.text.strip()
                        if author:
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract rating
                rating = ""
                try:
                    rating_elements = elem.find_elements(By.CSS_SELECTOR, "span, div")
                    for rating_elem in rating_elements:
                        text_content = rating_elem.text.strip()
                        if re.search(r'\d+\.\d+', text_content):  # Rating like 4.7
                            rating = text_content
                            break
                except Exception:
                    pass
                
                # Extract product (if available)
                product = "MyMuse Product"
                try:
                    product_elements = elem.find_elements(By.CSS_SELECTOR, "span, div")
                    for product_elem in product_elements:
                        text_content = product_elem.text.strip()
                        if any(keyword in text_content.lower() for keyword in ['groove', 'pulse', 'dive', 'edge', 'breeze']):
                            product = text_content
                            break
                except Exception:
                    pass
                
                # Create review object if we have meaningful data
                if text:
                    review = MyMuseReview(
                        author=author or f"Customer_{i+1}",
                        rating=rating or "5.0",
                        text=text,
                        product=product
                    )
                    reviews.append(review)
                    logger.info(f"Extracted review from: {author or f'Customer_{i+1}'}")
            
            except Exception as e:
                logger.warning(f"Error processing review {i}: {e}")
                continue
        
    except Exception as e:
        logger.error(f"Error extracting reviews: {e}")
    
    return reviews


def _extract_categories(driver) -> List[str]:
    """Extract product categories from the page."""
    categories = []
    
    try:
        # Look for category elements
        category_selectors = [
            "a[href*='collection']",
            "div[class*='category']",
            "span[class*='category']",
            "[data-testid='category']"
        ]
        
        for selector in category_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for elem in elements:
                        try:
                            text = elem.text.strip()
                            if text and len(text) > 2 and len(text) < 50:
                                if any(keyword in text.lower() for keyword in ['women', 'men', 'couple', 'massager', 'lubricant', 'toy']):
                                    categories.append(text)
                        except Exception:
                            continue
                    if categories:
                        logger.info(f"Found {len(categories)} categories using selector: {selector}")
                        break
            except Exception:
                continue
        
        # If no categories found, add default ones
        if not categories:
            categories = ["For Her", "For Him", "For Couples", "Massagers", "Lubricants", "Accessories"]
            logger.info("No categories found, using default categories")
        
    except Exception as e:
        logger.error(f"Error extracting categories: {e}")
        categories = ["For Her", "For Him", "For Couples"]
    
    return list(set(categories))  # Remove duplicates


def _extract_testimonials(driver) -> List[str]:
    """Extract customer testimonials and quotes from the page."""
    testimonials = []
    elements = []  # Initialize elements variable
    
    try:
        # Look for testimonial elements
        testimonial_selectors = [
            "div[class*='testimonial']",
            "div[class*='quote']",
            "blockquote",
            "[data-testid='testimonial']"
        ]
        
        for selector in testimonial_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for elem in elements:
                        try:
                            text = elem.text.strip()
                            if text and len(text) > 20 and len(text) < 500:
                                testimonials.append(text)
                        except Exception:
                            continue
                    if testimonials:
                        logger.info(f"Found {len(testimonials)} testimonials using selector: {selector}")
                        break
            except Exception:
                continue
        
        # If no testimonials found, try to find quote-like text
        if not testimonials:
            text_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, p")
            for elem in text_elements:
                try:
                    text = elem.text.strip()
                    if text and len(text) > 30 and len(text) < 400:
                        # Check if it looks like a testimonial
                        if any(keyword in text.lower() for keyword in ['love', 'amazing', 'perfect', 'recommend', 'happy', 'satisfied', 'best', 'great']):
                            if text not in testimonials:
                                testimonials.append(text)
                except Exception:
                    continue
        
    except Exception as e:
        logger.error(f"Error extracting testimonials: {e}")
    
    return testimonials


def convert_to_training_data(website_data: MyMuseWebsiteData, product_name: str = "mymuse") -> List[Dict[str, str]]:
    """Convert website data to training data format for the review index."""
    training_data = []
    
    # Add products
    for product in website_data.products:
        if product.description and len(product.description.strip()) > 10:
            training_data.append({
                "product_name": product_name,
                "text": f"{product.name}: {product.description}",
                "source": f"website_product_{product.name.lower().replace(' ', '_')}",
                "engagement": 0,
                "hashtags": []
            })
    
    # Add reviews
    for review in website_data.reviews:
        if review.text and len(review.text.strip()) > 10:
            training_data.append({
                "product_name": product_name,
                "text": f"Review: {review.text}",
                "source": f"website_review_{review.author.lower().replace(' ', '_')}",
                "engagement": 0,
                "hashtags": []
            })
    
    # Add testimonials
    for i, testimonial in enumerate(website_data.testimonials):
        if testimonial and len(testimonial.strip()) > 10:
            training_data.append({
                "product_name": product_name,
                "text": f"Testimonial: {testimonial}",
                "source": f"website_testimonial_{i}",
                "engagement": 0,
                "hashtags": []
            })
    
    return training_data


def save_training_data(training_data: List[Dict[str, str]], filename: str = "mymuse_website_training_data.csv") -> str:
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


def scrape_and_train(url: str = "https://mymuse.in/collections/deal-of-the-day", product_name: str = "mymuse") -> Dict[str, Any]:
    """
    Main function: scrape MyMuse website and convert to training data.
    Returns summary of the operation.
    """
    logger.info(f"Starting MyMuse website scrape from {url}")
    
    # Scrape website
    website_data = scrape_mymuse_website(url)
    if not website_data:
        return {"success": False, "error": "Failed to scrape website"}
    
    # Convert to training data
    training_data = convert_to_training_data(website_data, product_name)
    if not training_data:
        return {"success": False, "error": "No valid training data extracted"}
    
    # Save to CSV
    csv_path = save_training_data(training_data, f"mymuse_website_{int(time.time())}.csv")
    
    return {
        "success": True,
        "url": url,
        "products_scraped": len(website_data.products),
        "reviews_scraped": len(website_data.reviews),
        "testimonials_scraped": len(website_data.testimonials),
        "training_examples": len(training_data),
        "csv_path": csv_path,
        "categories": website_data.categories
    }
