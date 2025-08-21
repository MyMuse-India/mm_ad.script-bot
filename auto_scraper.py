from __future__ import annotations
import os
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

logger = logging.getLogger("mymuse")

# Configuration
AUTO_SCRAPE_ENABLED = os.getenv("AUTO_SCRAPE_ENABLED", "true").lower() in ("1", "true", "yes", "on")
AUTO_SCRAPE_INTERVAL = int(os.getenv("AUTO_SCRAPE_INTERVAL", "3600"))  # Default: 1 hour
MYMUSE_WEBSITE_URL = os.getenv("MYMUSE_WEBSITE_URL", "https://mymuse.in/collections/deal-of-the-day")
MAX_POSTS_PER_SCRAPE = int(os.getenv("MAX_POSTS_PER_SCRAPE", "100"))
DATA_DIR = os.getenv("DATA_DIR", "data")

class AutoScraper:
    """Automated Instagram scraper that runs in the background."""
    
    def __init__(self):
        self.is_running = False
        self.last_scrape_time: Optional[datetime] = None
        self.scrape_thread: Optional[threading.Thread] = None
        self.scrape_stats: Dict[str, Any] = {}
        
    def start(self):
        """Start the automated scraping service."""
        if self.is_running:
            logger.info("Auto-scraper is already running")
            return
            
        if not AUTO_SCRAPE_ENABLED:
            logger.info("Auto-scraping is disabled")
            return
            
        self.is_running = True
        self.scrape_thread = threading.Thread(target=self._run_scraping_loop, daemon=True)
        self.scrape_thread.start()
        logger.info("Auto-scraper started")
        
        # Run initial scrape immediately
        self._run_single_scrape()
        
    def stop(self):
        """Stop the automated scraping service."""
        self.is_running = False
        if self.scrape_thread:
            self.scrape_thread.join(timeout=5)
        logger.info("Auto-scraper stopped")
        
    def _run_scraping_loop(self):
        """Main scraping loop that runs continuously."""
        while self.is_running:
            try:
                # Wait for next scrape interval
                time.sleep(AUTO_SCRAPE_INTERVAL)
                
                if self.is_running:
                    self._run_single_scrape()
                    
            except Exception as e:
                logger.error(f"Error in scraping loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
                
    def _run_single_scrape(self):
        """Run a single scraping operation."""
        try:
            logger.info("Starting automated MyMuse website scrape")
            
            # Import here to avoid circular imports
            from mymuse_website_scraper import scrape_and_train
            
            # Run the scrape
            result = scrape_and_train(
                url=MYMUSE_WEBSITE_URL,
                product_name="mymuse"
            )
            
            if result.get("success"):
                # Auto-import into review index
                self._auto_import_training_data(result.get("csv_path", ""))
                
                # Update stats
                self.scrape_stats = {
                    "last_successful": datetime.now().isoformat(),
                    "products_scraped": result.get("products_scraped", 0),
                    "reviews_scraped": result.get("reviews_scraped", 0),
                    "testimonials_scraped": result.get("testimonials_scraped", 0),
                    "training_examples": result.get("training_examples", 0),
                    "csv_path": result.get("csv_path", ""),
                    "categories": result.get("categories", [])
                }
                
                self.last_scrape_time = datetime.now()
                logger.info(f"Automated website scrape completed successfully: {result.get('training_examples', 0)} training examples")
                
            else:
                logger.error(f"Automated website scrape failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Error during automated website scrape: {e}")
            
    def _auto_import_training_data(self, csv_path: str):
        """Automatically import scraped data into the review index."""
        if not csv_path or not os.path.exists(csv_path):
            logger.warning(f"CSV file not found: {csv_path}")
            return
            
        try:
            from review_store import ReviewIndex
            
            # Import the new data
            info = ReviewIndex.import_csv_file(csv_path)
            ReviewIndex.build()
            
            logger.info(f"Auto-imported {info.get('added', 0)} new training examples into review index")
            
        except Exception as e:
            logger.error(f"Failed to auto-import training data: {e}")
            
    def get_status(self) -> Dict[str, Any]:
        """Get current scraper status."""
        return {
            "is_running": self.is_running,
            "enabled": AUTO_SCRAPE_ENABLED,
            "interval_seconds": AUTO_SCRAPE_INTERVAL,
            "last_scrape": self.last_scrape_time.isoformat() if self.last_scrape_time else None,
            "stats": self.scrape_stats,
            "target_website": MYMUSE_WEBSITE_URL
        }
        
    def force_scrape(self):
        """Force an immediate scrape (can be called from admin or API)."""
        if not self.is_running:
            logger.warning("Auto-scraper is not running")
            return False
            
        try:
            self._run_single_scrape()
            return True
        except Exception as e:
            logger.error(f"Forced scrape failed: {e}")
            return False


# Global instance
auto_scraper = AutoScraper()


def start_auto_scraper():
    """Start the automated scraper service."""
    auto_scraper.start()


def stop_auto_scraper():
    """Stop the automated scraper service."""
    auto_scraper.stop()


def get_scraper_status() -> Dict[str, Any]:
    """Get the current scraper status."""
    return auto_scraper.get_status()


def force_scrape_now() -> bool:
    """Force an immediate scrape."""
    return auto_scraper.force_scrape()


# Auto-start when module is imported (if enabled)
if AUTO_SCRAPE_ENABLED:
    # Start in a separate thread to avoid blocking
    startup_thread = threading.Thread(target=start_auto_scraper, daemon=True)
    startup_thread.start()
