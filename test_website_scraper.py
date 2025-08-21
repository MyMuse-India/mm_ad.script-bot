#!/usr/bin/env python3
"""
Test script for MyMuse website scraper to debug issues.
"""

import logging
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_website_scraper():
    """Test the MyMuse website scraper."""
    try:
        from mymuse_website_scraper import scrape_mymuse_website, scrape_and_train
        
        print("Testing MyMuse website scraper...")
        print("=" * 50)
        
        # Test direct website scraping
        print("1. Testing website scraping...")
        website_data = scrape_mymuse_website("https://mymuse.in/collections/deal-of-the-day")
        
        if website_data:
            print(f"✅ Website scraped successfully!")
            print(f"   Products found: {len(website_data.products)}")
            print(f"   Reviews found: {len(website_data.reviews)}")
            print(f"   Testimonials found: {len(website_data.testimonials)}")
            print(f"   Categories found: {len(website_data.categories)}")
            print(f"   Total items: {website_data.total_items}")
            
            if website_data.products:
                print("\n   Sample products:")
                for i, product in enumerate(website_data.products[:3]):
                    print(f"   {i+1}. {product.name}: {product.description[:100]}...")
            
            if website_data.reviews:
                print("\n   Sample reviews:")
                for i, review in enumerate(website_data.reviews[:2]):
                    print(f"   {i+1}. {review.author}: {review.text[:100]}...")
            
            if website_data.testimonials:
                print("\n   Sample testimonials:")
                for i, testimonial in enumerate(website_data.testimonials[:2]):
                    print(f"   {i+1}. {testimonial[:100]}...")
        else:
            print("❌ Website scraping failed")
        
        print("\n" + "=" * 50)
        
        # Test full scrape and train
        print("2. Testing full scrape and train...")
        result = scrape_and_train("https://mymuse.in/collections/deal-of-the-day", "mymuse")
        
        if result.get("success"):
            print(f"✅ Full scrape successful!")
            print(f"   Products scraped: {result.get('products_scraped', 0)}")
            print(f"   Reviews scraped: {result.get('reviews_scraped', 0)}")
            print(f"   Testimonials scraped: {result.get('testimonials_scraped', 0)}")
            print(f"   Training examples: {result.get('training_examples', 0)}")
            print(f"   CSV path: {result.get('csv_path', 'N/A')}")
            print(f"   Categories: {', '.join(result.get('categories', []))}")
        else:
            print(f"❌ Full scrape failed: {result.get('error', 'Unknown error')}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install selenium webdriver-manager")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_website_scraper()
