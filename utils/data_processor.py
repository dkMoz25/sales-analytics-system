
"""
Part 2: Data Processing
Performs comprehensive analysis on sales data
"""

from collections import defaultdict
from datetime import datetime


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    
    Returns: float (total revenue)
    """
    total = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    return total


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    
    Returns: dictionary with region statistics
    """
    region_data = defaultdict(lambda: {'total_sales': 0, 'transaction_count': 0})
    
    total_revenue = calculate_total_revenue(transactions)
    
    for t in transactions:
        region = t['Region']
        sales = t['Quantity'] * t['UnitPrice']
        region_data[region]['total_sales'] += sales
        region_data[region]['transaction_count'] += 1
    
    # Calculate percentages and sort
    result = {}
    for region, data in region_data.items():
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': round((data['total_sales'] / total_revenue * 100), 2) if total_revenue > 0 else 0
        }
    
    # Sort by total_sales descending
    result = dict(sorted(result.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
    
    for t in transactions:
        product = t['ProductName']
        product_data[product]['quantity'] += t['Quantity']
        product_data[product]['revenue'] += t['Quantity'] * t['UnitPrice']
    
    # Convert to list of tuples and sort
    products = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]
    
    products.sort(key=lambda x: x[1], reverse=True)
    
    return products[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    
    Returns: dictionary of customer statistics
    """
    customer_data = defaultdict(lambda: {
        'total_spent': 0,
        'purchase_count': 0,
        'products_bought': set()
    })
    
    for t in transactions:
        customer = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(t['ProductName'])
    
    # Calculate average and convert to final format
    result = {}
    for customer, data in customer_data.items():
        result[customer] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': sorted(list(data['products_bought']))
        }
    
    # Sort by total_spent descending
    result = dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    return result


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Returns: dictionary sorted by date
    """
    daily_data = defaultdict(lambda: {
        'revenue': 0,
        'transaction_count': 0,
        'customers': set()
    })
    
    for t in transactions:
        date = t['Date']
        daily_data[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(t['CustomerID'])
    
    # Convert to final format
    result = {}
    for date, data in daily_data.items():
        result[date] = {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
    
    # Sort chronologically
    result = dict(sorted(result.items()))
    
    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_trend = daily_sales_trend(transactions)
    
    if not daily_trend:
        return None
    
    peak_date = max(daily_trend.items(), key=lambda x: x[1]['revenue'])
    
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
    
    for t in transactions:
        product = t['ProductName']
        product_data[product]['quantity'] += t['Quantity']
        product_data[product]['revenue'] += t['Quantity'] * t['UnitPrice']
    
    # Filter and convert to list
    low_performers = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
        if data['quantity'] < threshold
    ]
    
    # Sort by quantity ascending
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers

