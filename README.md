# 🛒 Grocery Price Scraper

Simple Python web scraper to compare grocery prices across Indian delivery platforms.

## What it does
- Scrapes product prices from Blinkit, Zepto, and Swiggy Instamart
- Saves data to CSV files for comparison
- Helps find cheaper alternatives across platforms

## Current Status
- ✅ Blinkit scraper - Working
- ✅ Zepto scraper - Working  
- ⚠️ Swiggy scraper - In progress (anti-scraping challenges)

## Files
- `blinkit_scraper.py` - Scrapes Blinkit products
- `zepto_scraper.py` - Scrapes Zepto products
- `swiggy_scraper.py` - Swiggy scraper (WIP)
- CSV files with scraped product data

## Requirements
```bash
pip install selenium pandas webdriver-manager
```

## Usage
```bash
python blinkit_scraper.py
# Follow prompts to set location and search products
```

## Sample Output
```
✅ Product 1: Amul Milk 1L - ₹65
✅ Product 2: Mother Dairy Milk 1L - ₹62
📊 Found 15 products
💾 Results saved to: blinkit_milk_results.csv
```

## Tech Stack
- Python 3.12
- Selenium WebDriver
- Pandas
- Chrome/Safari automation

## Next Steps
- [ ] Fix Swiggy scraper
- [ ] Add price comparison analysis
- [ ] Create database for historical tracking
- [ ] Build visualization dashboard

## Note
Built for educational purposes. Includes manual assistance for location setting and product search due to anti-bot measures on these platforms.

---
*Personal project to learn web scraping and help with grocery shopping decisions.*