
"""
Part 1: Data File Handler & Preprocessing
Handles reading, parsing, and validating sales data
"""

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                # Skip header and remove empty lines
                raw_lines = [line.strip() for line in lines[1:] if line.strip()]
                return raw_lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    
    print(f"Error: Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Returns: list of dictionaries with transaction data
    """
    transactions = []
    
    for line in raw_lines:
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue
        
        try:
            # Clean ProductName - remove commas
            product_name = parts[3].replace(',', ' ')
            
            # Clean numeric fields - remove commas and convert
            quantity_str = parts[4].replace(',', '')
            unit_price_str = parts[5].replace(',', '')
            
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': product_name.strip(),
                'Quantity': int(quantity_str),
                'UnitPrice': float(unit_price_str),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            
            transactions.append(transaction)
            
        except (ValueError, IndexError):
            # Skip rows with conversion errors
            continue
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0
    
    # Validation
    for transaction in transactions:
        # Validation rules
        if (transaction['Quantity'] <= 0 or
            transaction['UnitPrice'] <= 0 or
            not transaction['CustomerID'] or
            not transaction['Region'] or
            not transaction['TransactionID'].startswith('T') or
            not transaction['ProductID'].startswith('P') or
            not transaction['CustomerID'].startswith('C')):
            invalid_count += 1
        else:
            valid_transactions.append(transaction)
    
    # Display available options
    if valid_transactions:
        regions = sorted(set(t['Region'] for t in valid_transactions))
        print(f"
Available Regions: {', '.join(regions)}")
        
        amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
        print(f"Transaction Amount Range: ₹{min(amounts):.2f} - ₹{max(amounts):.2f}")
    
    # Apply filters
    filtered_transactions = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0
    
    if region:
        before_filter = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        filtered_by_region = before_filter - len(filtered_transactions)
        print(f"
After region filter ({region}): {len(filtered_transactions)} records")
    
    if min_amount is not None or max_amount is not None:
        before_filter = len(filtered_transactions)
        filtered_transactions = [
            t for t in filtered_transactions
            if (min_amount is None or t['Quantity'] * t['UnitPrice'] >= min_amount) and
               (max_amount is None or t['Quantity'] * t['UnitPrice'] <= max_amount)
        ]
        filtered_by_amount = before_filter - len(filtered_transactions)
        print(f"After amount filter: {len(filtered_transactions)} records")
    
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    return filtered_transactions, invalid_count, filter_summary

