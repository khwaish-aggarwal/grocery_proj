from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class SwiggyManualScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver"""
        print("🚀 Setting up Chrome driver for Swiggy manual extraction...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("✅ Chrome ready!")
    
    def open_swiggy_and_extract(self):
        """Open Swiggy and do manual product entry"""
        print("🌐 Opening Swiggy Instamart...")
        self.driver.get("https://www.swiggy.com/instamart")
        time.sleep(5)
        
        print("\n" + "="*60)
        print("📝 MANUAL PRODUCT ENTRY FOR SWIGGY INSTAMART")
        print("="*60)
        print("Since Swiggy has complex JavaScript rendering,")
        print("we'll manually enter the products you see on screen.")
        print("="*60)
        
        # Ask for product type
        product_type = input("🔍 What product are you looking for? (e.g., milk, bread): ").strip()
        if not product_type:
            product_type = "product"
        
        print(f"\n📋 Now manually enter the {product_type} products you see on Swiggy:")
        print("For each product, enter the name and price.")
        print("Press Enter with empty name when you're done.")
        print("-" * 50)
        
        products = []
        product_count = 1
        
        while True:
            print(f"\n🛒 Product #{product_count}:")
            
            # Get product name
            name = input("  Product name (or press Enter to finish): ").strip()
            if not name:
                break
            
            # Get product price
            price = input("  Product price (e.g., ₹67, ₹45): ").strip()
            if not price and '₹' not in price:
                price = input("  Please enter price with ₹ symbol: ").strip()
            
            # Get optional size/quantity
            size = input("  Size/Quantity (optional, e.g., 1L, 500g): ").strip()
            
            # Create product entry
            product = {
                'platform': 'Swiggy Instamart',
                'name': name,
                'price': price,
                'size': size if size else 'N/A',
                'url': self.driver.current_url,
                'entry_method': 'Manual'
            }
            
            products.append(product)
            print(f"  ✅ Added: {name} - {price}")
            product_count += 1
        
        return products, product_type
    
    def verify_products(self, products):
        """Show products for verification"""
        if not products:
            return products
        
        print(f"\n📋 You entered {len(products)} products:")
        print("-" * 60)
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['name']} - {product['price']}")
            if product['size'] != 'N/A':
                print(f"   Size: {product['size']}")
        
        print("-" * 60)
        
        # Ask for confirmation
        confirm = input("\n✅ Are these products correct? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("❌ Let's edit the products...")
            return self.edit_products(products)
        
        return products
    
    def edit_products(self, products):
        """Allow editing of entered products"""
        while True:
            print(f"\n📝 Edit products (you have {len(products)} products):")
            print("1. Add more products")
            print("2. Remove a product")
            print("3. Edit a product")
            print("4. Done editing")
            
            choice = input("Your choice (1-4): ").strip()
            
            if choice == '1':
                # Add more products
                print("\n➕ Adding more products:")
                count = len(products) + 1
                
                while True:
                    name = input(f"  Product #{count} name (or Enter to stop): ").strip()
                    if not name:
                        break
                    
                    price = input("  Price: ").strip()
                    size = input("  Size (optional): ").strip()
                    
                    product = {
                        'platform': 'Swiggy Instamart',
                        'name': name,
                        'price': price,
                        'size': size if size else 'N/A',
                        'url': self.driver.current_url,
                        'entry_method': 'Manual'
                    }
                    
                    products.append(product)
                    print(f"  ✅ Added: {name}")
                    count += 1
            
            elif choice == '2':
                # Remove a product
                if not products:
                    print("❌ No products to remove")
                    continue
                
                print("\n➖ Remove a product:")
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product['name']} - {product['price']}")
                
                try:
                    index = int(input("Enter number to remove: ")) - 1
                    if 0 <= index < len(products):
                        removed = products.pop(index)
                        print(f"✅ Removed: {removed['name']}")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            elif choice == '3':
                # Edit a product
                if not products:
                    print("❌ No products to edit")
                    continue
                
                print("\n✏️ Edit a product:")
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product['name']} - {product['price']}")
                
                try:
                    index = int(input("Enter number to edit: ")) - 1
                    if 0 <= index < len(products):
                        product = products[index]
                        print(f"Editing: {product['name']}")
                        
                        new_name = input(f"New name (current: {product['name']}): ").strip()
                        if new_name:
                            product['name'] = new_name
                        
                        new_price = input(f"New price (current: {product['price']}): ").strip()
                        if new_price:
                            product['price'] = new_price
                        
                        new_size = input(f"New size (current: {product['size']}): ").strip()
                        if new_size:
                            product['size'] = new_size
                        
                        print("✅ Product updated")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            elif choice == '4':
                break
            
            else:
                print("❌ Invalid choice")
        
        return products
    
    def save_results(self, products, product_type):
        """Save results to CSV"""
        if not products:
            print("❌ No products to save")
            return
        
        try:
            # Create filename
            clean_name = "".join(c for c in product_type if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_name = clean_name.replace(' ', '_').lower()
            filename = f"swiggy_instamart_{clean_name}_manual_results.csv"
            
            df = pd.DataFrame(products)
            
            # Display results
            print("\n" + "="*80)
            print(f"🎉 SWIGGY INSTAMART {product_type.upper()} PRODUCTS (MANUAL ENTRY)")
            print("="*80)
            
            # Show clean results
            display_columns = ['name', 'price']
            if any(p['size'] != 'N/A' for p in products):
                display_columns.append('size')
            
            display_df = df[display_columns].copy()
            print(display_df.to_string(index=False))
            
            # Save to file
            df.to_csv(filename, index=False)
            print(f"\n💾 Results saved to: {filename}")
            
            # Summary
            print(f"\n📈 SUMMARY:")
            print(f"   Total products: {len(products)}")
            print(f"   Product type: {product_type}")
            print(f"   File saved: {filename}")
            print(f"   Platform: Swiggy Instamart")
            print(f"   Method: Manual Entry")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_manual_scraper(self):
        """Main workflow"""
        try:
            # Open Swiggy and get manual input
            products, product_type = self.open_swiggy_and_extract()
            
            if not products:
                print("❌ No products entered")
                return
            
            # Verify products
            products = self.verify_products(products)
            
            # Save results
            self.save_results(products, product_type)
            
            return products
            
        except Exception as e:
            print(f"❌ Error in manual scraper: {e}")
            return []
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function"""
    print("🛒 Swiggy Instamart Manual Product Entry Tool")
    print("Since Swiggy has complex anti-scraping measures,")
    print("this tool helps you manually enter product data.")
    print("="*60)
    
    scraper = SwiggyManualScraper()
    
    try:
        products = scraper.run_manual_scraper()
        
        if products:
            print(f"\n🎉 SUCCESS! Manually entered {len(products)} products from Swiggy Instamart")
            print("📁 Data saved and ready for price comparison!")
        else:
            print(f"\n😞 No products were entered")
            
    except KeyboardInterrupt:
        print("\n⏹️ Process stopped by user")
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