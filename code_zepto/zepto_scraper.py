from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class ZeptoScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver"""
        print("🚀 Setting up Chrome driver for Zepto...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("✅ Chrome ready for Zepto!")
    
    def open_zepto(self):
        """Open Zepto and wait for manual setup"""
        print("🌐 Opening Zepto...")
        self.driver.get("https://www.zepto.com/")
        time.sleep(5)
        
        print("\n" + "="*60)
        print("📍 ZEPTO MANUAL SETUP")
        print("="*60)
        print("Please complete these steps manually in the browser:")
        print("1. Set your delivery location")
        print("2. Handle any login prompts (you can skip if possible)")
        print("3. Search for ANY product you want")
        print("4. Wait for products to appear on the page")
        print("5. Then come back here and continue")
        print("\nNote: Zepto might require phone number verification")
        print("="*60)
        
        # Ask user what they searched for
        product_searched = input("🔍 What product did you search for? (e.g., milk, bread, eggs): ").strip()
        
        if not product_searched:
            product_searched = "product"  # fallback
        
        input(f"✅ Press Enter after you've searched for '{product_searched}' and can see the products...")
        print(f"🔍 Now looking for {product_searched} products on Zepto...")
        
        return product_searched
    
    def extract_products_simple(self, max_products=None):
        """Extract products from Zepto"""
        products = []
        
        try:
            # Give page time to load
            time.sleep(3)
            
            print(f"📄 Current page: {self.driver.current_url}")
            print(f"📝 Page title: {self.driver.title}")
            
            # Find all elements with rupee symbol
            print("💰 Looking for price elements...")
            price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '₹')]")
            print(f"Found {len(price_elements)} elements with prices")
            
            if not price_elements:
                print("❌ No price elements found!")
                print("Make sure you're on a page with products visible")
                return []
            
            # Set max products limit
            if max_products is None:
                max_products = len(price_elements)
                print(f"🎯 Extracting ALL products found (up to {max_products})")
            else:
                print(f"🎯 Extracting up to {max_products} products")
            
            # Extract products from price elements
            seen_products = set()
            
            for i, price_elem in enumerate(price_elements):
                try:
                    # Get different parent containers to find product info
                    parents_to_try = [
                        "../..",           # grandparent
                        "../../..",        # great-grandparent  
                        "../../../..",     # great-great-grandparent
                        "../../../../..",  # great-great-great-grandparent
                    ]
                    
                    for parent_path in parents_to_try:
                        try:
                            container = price_elem.find_element(By.XPATH, parent_path)
                            container_text = container.text.strip()
                            
                            # Skip if empty or too short
                            if not container_text or len(container_text) < 10:
                                continue
                            
                            # Skip if we've seen this product already
                            if container_text in seen_products:
                                continue
                            
                            # Check if it looks like a product (has name and price)
                            lines = container_text.split('\n')
                            
                            # Extract product name and price
                            product_name = None
                            product_price = None
                            
                            for line in lines:
                                line = line.strip()
                                if '₹' in line and not product_price:
                                    product_price = line
                                elif (line and 
                                      '₹' not in line and 
                                      'ADD' not in line.upper() and 
                                      'SAVE' not in line.upper() and
                                      'OFF' not in line.upper() and
                                      'MIN' not in line.upper() and
                                      len(line) > 3 and
                                      not line.isdigit() and
                                      not product_name):
                                    product_name = line
                            
                            # If we found both name and price, it's a valid product
                            if product_name and product_price:
                                product = {
                                    'platform': 'Zepto',
                                    'name': product_name,
                                    'price': product_price,
                                    'full_text': container_text,
                                    'url': self.driver.current_url
                                }
                                
                                products.append(product)
                                seen_products.add(container_text)
                                
                                print(f"✅ Product {len(products)}: {product_name[:40]}... - {product_price}")
                                break
                                
                        except Exception:
                            continue
                    
                    # Stop if we reached the limit
                    if len(products) >= max_products:
                        print(f"🛑 Reached limit of {max_products} products")
                        break
                        
                except Exception as e:
                    continue
            
            print(f"\n📊 Found {len(products)} total products")
            return products
            
        except Exception as e:
            print(f"❌ Error extracting products: {e}")
            return []
    
    def save_results(self, products, product_name, filename=None):
        """Save results to CSV with dynamic filename"""
        if not products:
            print("❌ No products to save")
            return
        
        try:
            # Create filename based on product searched
            if filename is None:
                clean_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_name = clean_name.replace(' ', '_').lower()
                filename = f"zepto_{clean_name}_results.csv"
            
            df = pd.DataFrame(products)
            
            # Display results
            print("\n" + "="*80)
            print(f"🎉 ZEPTO {product_name.upper()} PRODUCTS FOUND")
            print("="*80)
            
            # Show clean results
            display_df = df[['name', 'price']].copy()
            print(display_df.to_string(index=False))
            
            # Save to file
            df.to_csv(filename, index=False)
            print(f"\n💾 Full results saved to: {filename}")
            
            # Summary
            print(f"\n📈 SUMMARY:")
            print(f"   Total products: {len(products)}")
            print(f"   Product searched: {product_name}")
            print(f"   File saved: {filename}")
            print(f"   Platform: Zepto")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_scraper(self):
        """Main scraper workflow"""
        try:
            # Step 1: Open Zepto and wait for manual setup
            product_searched = self.open_zepto()
            
            # Step 2: Extract products
            print(f"\n🔢 How many {product_searched} products do you want to extract?")
            print("1. Enter a number (e.g., 20)")
            print("2. Press Enter for ALL products on the page")
            
            user_input = input("Your choice: ").strip()
            
            if user_input.isdigit():
                max_products = int(user_input)
                print(f"🎯 Will extract up to {max_products} products")
            else:
                max_products = None
                print("🎯 Will extract ALL products found")
            
            products = self.extract_products_simple(max_products)
            
            # Step 3: Save results
            if products:
                self.save_results(products, product_searched)
            else:
                print(f"\n❌ No {product_searched} products were found!")
                print("Troubleshooting tips:")
                print(f"- Make sure you searched for '{product_searched}' on Zepto")
                print("- Ensure products are visible on the page")
                print("- Check that you're not on a 'no results' page")
                print("- Try scrolling down to load more products")
                print("- Zepto might require phone verification")
            
            return products, product_searched
            
        except Exception as e:
            print(f"❌ Error in main scraper: {e}")
            return [], "unknown"
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function"""
    print("🛒 Zepto Universal Product Scraper")
    print("This scraper works with ANY product you want to search!")
    print("="*60)
    
    scraper = ZeptoScraper()
    
    try:
        products, product_name = scraper.run_scraper()
        
        if products:
            print(f"\n🎉 SUCCESS! Found {len(products)} {product_name} products on Zepto")
            print(f"📁 Results saved to: zepto_{product_name.lower().replace(' ', '_')}_results.csv")
        else:
            print(f"\n😞 No {product_name} products found. Try running again and make sure:")
            print(f"   - Zepto loads properly")
            print(f"   - You can set your location") 
            print(f"   - Search for '{product_name}' works")
            print(f"   - Products are visible on the page")
            
    except KeyboardInterrupt:
        print("\n⏹️ Scraper stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    finally:
        print("\n" + "="*60)
        print("Press Enter to close browser...")
        input()
        scraper.close()
        print("👋 Browser closed. Goodbye!")

if __name__ == "__main__":
    main()