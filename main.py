import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import quote
import json

def download_image(url, folder_name, filename):
    """Download image from URL with custom filename"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'png' in content_type:
                ext = 'png'
            elif 'gif' in content_type:
                ext = 'gif'
            elif 'webp' in content_type:
                ext = 'webp'
            else:
                ext = 'jpg'
            
            filepath = os.path.join(folder_name, f"{filename}.{ext}")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  ✓ Saved as: {filename}.{ext}")
            return True
    except Exception as e:
        print(f"  ✗ Error downloading: {e}")
    return False

def scrape_bing_images(query, folder_name, filename):
    """Scrape single image from Bing Images"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        search_url = f"https://www.bing.com/images/search?q={quote(query)}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_links = soup.find_all('a', class_='iusc')
        
        if not img_links:
            return False
        
        for link in img_links:
            try:
                m_json = link.get('m')
                if m_json:
                    data = json.loads(m_json)
                    img_url = data.get('murl') or data.get('turl')
                    
                    if img_url:
                        if download_image(img_url, folder_name, filename):
                            time.sleep(0.5)
                            return True
            except Exception as e:
                continue
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def scrape_products_by_category(categories):
    """Scrape images for products organized by category"""
    
    print("=" * 60)
    print("🖼️  CATEGORY-BASED IMAGE SCRAPER")
    print("=" * 60)
    print()
    
    total_downloaded = 0
    
    for category, products in categories.items():
        print(f"\n📂 Category: {category.upper()}")
        print("-" * 60)
        
        # Create main category folder only
        category_folder = f"images_{category.replace(' ', '_')}"
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        
        for product_name in products:
            print(f"\n🔍 Searching: {product_name}")
            
            # Use product name as filename (clean it)
            safe_filename = product_name.replace('/', '-').replace('\\', '-')
            
            # Download image directly to category folder
            if scrape_bing_images(product_name, category_folder, safe_filename):
                total_downloaded += 1
                print(f"  ✅ Saved to {category_folder}/")
            else:
                print(f"  ⚠️ No image downloaded for {product_name}")
    
    print("\n" + "=" * 60)
    print(f"✅ TOTAL: {total_downloaded} images downloaded!")
    print("=" * 60)

# ====================================================================
# DITO MO ILAGAY ANG MGA PRODUCTS PER CATEGORY
# ====================================================================

if __name__ == "__main__":
    
    # Format: Simple list of product names
    categories = {
       'medicine': [
   
#dito ilalalagay ang mga products example:    
#           'Paracetamol 500mg',       
#            'Ibuprofen 200mg', 


],
    
    }
    
    # Run the scraper
    scrape_products_by_category(categories)
    
    print("\n📌 PAANO GAMITIN:")
    print("   1. I-edit ang 'categories' dictionary")
    print("   2. Dagdagan ng category kung gusto")
    print("   3. Dagdag lang ng product names sa list")
    print("\n   Example:")
    print("   'personal_care': [")
    print("       'Lipstick Red',")
    print("       'Face Powder',")
    print("       'Nail Polish',")
    print("   ]")