#!/usr/bin/env python3
"""
Test script for Instagram scraper to debug issues.
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

def test_instagram_scraper():
    """Test the Instagram scraper with MyMuse profile."""
    try:
        from instagram_scraper import scrape_instagram_profile, scrape_and_train
        
        print("Testing Instagram scraper...")
        print("=" * 50)
        
        # Test direct profile scraping
        print("1. Testing profile scraping...")
        profile = scrape_instagram_profile("mymuse.in", max_posts=10)
        
        if profile:
            print(f"✅ Profile scraped successfully!")
            print(f"   Username: @{profile.username}")
            print(f"   Full Name: {profile.full_name}")
            print(f"   Bio: {profile.bio[:100]}...")
            print(f"   Posts found: {len(profile.posts)}")
            print(f"   Followers: {profile.followers_count}")
            
            if profile.posts:
                print("\n   Sample posts:")
                for i, post in enumerate(profile.posts[:3]):
                    print(f"   {i+1}. {post.caption[:100]}...")
            else:
                print("   ❌ No posts found")
        else:
            print("❌ Profile scraping failed")
        
        print("\n" + "=" * 50)
        
        # Test full scrape and train
        print("2. Testing full scrape and train...")
        result = scrape_and_train("mymuse.in", "mymuse", max_posts=10)
        
        if result.get("success"):
            print(f"✅ Full scrape successful!")
            print(f"   Posts scraped: {result.get('posts_scraped', 0)}")
            print(f"   Training examples: {result.get('training_examples', 0)}")
            print(f"   CSV path: {result.get('csv_path', 'N/A')}")
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
    test_instagram_scraper()
