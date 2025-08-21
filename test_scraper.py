from selenium_scraper import scrape_reviews

url = "https://mymuse.in/products/dive-plus-app-controlled-massager"
revs = scrape_reviews(url)

print("COUNT:", len(revs))
for r in revs[:5]:
    print("-", r)
