
"""
Part 5: Main Application
Orchestrates the entire sales analytics workflow
"""

import sys
sys.path.append('utils')

from file_handler import read_sales_data, parse_transactions, validate_and_filter
from data_processor import *
from api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from report_generator import generate_sales_report


def main():
    """
    Main execution function
    """
    try:
        print("=" * 70)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 70)
        print()
        
        # Step 1: Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("✗ Failed to read data file")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions
")
        
        # Step 2: Parse and clean data
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records
")
        
        # Step 3: Filter options
        print("[3/10] Filter Options Available:")
        valid_trans, invalid_count, summary = validate_and_filter(transactions)
        
        filter_choice = input("
Do you want to filter data? (y/n): ").strip().lower()
        
        if filter_choice == 'y':
            region_filter = input("Enter region to filter (or press Enter to skip): ").strip()
            region_filter = region_filter if region_filter else None
            
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            min_amt = float(min_amt) if min_amt else None
            
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()
            max_amt = float(max_amt) if max_amt else None
            
            valid_trans, invalid_count, summary = validate_and_filter(
                transactions, region_filter, min_amt, max_amt
            )
        
        # Step 4: Validate transactions
        print(f"
[4/10] Validating transactions...")
        print(f"✓ Valid: {summary['final_count']} | Invalid: {invalid_count}
")
        
        # Step 5: Analyze sales data
        print("[5/10] Analyzing sales data...")
        total_rev = calculate_total_revenue(valid_trans)
        region_stats = region_wise_sales(valid_trans)
        top_prods = top_selling_products(valid_trans)
        cust_analysis = customer_analysis(valid_trans)
        daily_trend = daily_sales_trend(valid_trans)
        peak_day = find_peak_sales_day(valid_trans)
        low_prods = low_performing_products(valid_trans)
        print("✓ Analysis complete
")
        
        # Step 6: Fetch product data from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print()
        
        # Step 7: Enrich sales data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_trans = enrich_sales_data(valid_trans, product_mapping)
        enriched_count = sum(1 for t in enriched_trans if t.get('API_Match', False))
        success_rate = (enriched_count / len(enriched_trans) * 100) if enriched_trans else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_trans)} transactions ({success_rate:.1f}%)
")
        
        # Step 8: Save enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_trans)
        print()
        
        # Step 9: Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_trans, enriched_trans)
        print()
        
        # Step 10: Complete
        print("[10/10] Process Complete!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("

✗ Process interrupted by user")
    except Exception as e:
        print(f"
✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

