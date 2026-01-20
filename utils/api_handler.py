
"""
Part 3: API Integration
Fetches product data from DummyJSON API and enriches sales data
"""

import requests
import re


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns: list of product dictionaries
    """
    try:
        url = 'https://dummyjson.com/products?limit=100'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        print(f"✓ Successfully fetched {len(products)} products from API")
        
        # Extract relevant fields
        simplified_products = [
            {
                'id': p['id'],
                'title': p['title'],
                'category': p['category'],
                'brand': p.get('brand', 'Unknown'),
                'price': p['price'],
                'rating': p['rating']
            }
            for p in products
        ]
        
        return simplified_products
        
    except requests.exceptions.RequestException as e:
        print(f"✗ API Error: {e}")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    
    Returns: dictionary mapping product IDs to info
    """
    mapping = {}
    
    for product in api_products:
        product_id = product['id']
        mapping[product_id] = {
            'title': product['title'],
            'category': product['category'],
            'brand': product['brand'],
            'rating': product['rating']
        }
    
    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    
    Returns: list of enriched transaction dictionaries
    """
    enriched_transactions = []
    
    for transaction in transactions:
        enriched = transaction.copy()
        
        # Extract numeric ID from ProductID (P101 -> 101, P5 -> 5)
        try:
            product_id_str = transaction['ProductID']
            numeric_id = int(re.search(r'\d+', product_id_str).group())
            
            if numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]
                enriched['API_Category'] = product_info['category']
                enriched['API_Brand'] = product_info['brand']
                enriched['API_Rating'] = product_info['rating']
                enriched['API_Match'] = True
            else:
                enriched['API_Category'] = None
                enriched['API_Brand'] = None
                enriched['API_Rating'] = None
                enriched['API_Match'] = False
                
        except (AttributeError, ValueError):
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False
        
        enriched_transactions.append(enriched)
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    try:
        # Create directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as file:
            # Write header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
"
            file.write(header)
            
            # Write data
            for t in enriched_transactions:
                line = f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|"
                line += f"{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|"
                line += f"{t.get('API_Category', '')}|{t.get('API_Brand', '')}|"
                line += f"{t.get('API_Rating', '')}|{t.get('API_Match', False)}
"
                file.write(line)
        
        print(f"✓ Enriched data saved to: {filename}")
        
    except Exception as e:
        print(f"✗ Error saving enriched data: {e}")

