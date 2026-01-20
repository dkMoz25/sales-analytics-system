
---Sales Analytics System---

A comprehensive Python-based sales data analytics system that processes sales transactions, integrates with external APIs, performs in-depth analysis, and generates detailed reports.

Student Name: Dhiraj Kumar Singh

Student ID: bitsom_ba_25071009

Email: singhdhiraj255@gmail.com

Date: 20th Jan'26

Project Overview:
This project is a complete sales analytics solution that:
Processes raw sales data with robust error handling
Validates and filters transactions based on multiple criteria
Performs comprehensive sales analysis across regions, products, and customers
Integrates with DummyJSON API to enrich product information
Generates professional formatted reports
Handles data quality issues including encoding problems and missing values

✨ Features -
🔧 Data Processing
Multi-encoding support: Handles UTF-8, Latin-1, and CP1252 encodings
Data cleaning: Removes commas from numeric fields and product names
Validation: Filters invalid transactions (negative values, missing fields, incorrect IDs)
Flexible filtering: Optional region and amount-based filtering

📊 Analytics Capabilities
Revenue Analysis: Total revenue calculation and average order values
Regional Performance: Sales breakdown by geographic region with percentages
Product Insights: Top-selling and low-performing product identification
Customer Analysis: Purchase patterns, spending habits, and loyalty metrics
Temporal Trends: Daily sales patterns and peak sales day identification

🌐 API Integration
External Data Enrichment: Fetches product data from DummyJSON API
Smart Mapping: Matches internal product IDs with external API data
Graceful Degradation: Handles API failures without breaking the workflow
Data Augmentation: Adds category, brand, and rating information

📄 Report Generation
Comprehensive Reports: Professional formatted text reports with multiple sections
Visual Formatting: Clear tables and structured layouts
Multiple Metrics: Includes summary statistics, trends, and performance indicators
Export Ready: Saves reports to easily shareable text files

& Modular code organization.

How to Run the Code:

To run the Sales Analytics System, first ensure Python 3.7 or higher and pip are installed on your system, along with an active internet connection for API integration. Navigate to the project root directory (sales-analytics-system/) and install the required dependency by running pip install -r requirements.txt, which installs the requests library needed for API calls. Once setup is complete, execute the program by running python main.py from the terminal. The system will automatically process through 10 sequential steps: reading and parsing the sales data file, offering optional filtering by region or transaction amount (enter 'n' to process all data for full evaluation), validating transactions to filter out invalid records, performing comprehensive analytics including revenue calculations and trend analysis, fetching product data from the DummyJSON API, enriching the sales data with API information, saving the enriched dataset to data/enriched_sales_data.txt, generating a detailed report at output/sales_report.txt, and displaying a completion message. The entire execution takes approximately 5-10 seconds and produces two output files for evaluation: the enriched sales data file containing API-enhanced information with additional columns for category, brand, and rating, and the comprehensive sales report containing eight sections covering overall summary, regional performance, top products and customers, daily trends, and API enrichment statistics. If any errors occur such as missing files or module import issues, ensure the sales_data.txt file is in the data/ folder and all dependencies are properly installed. The program includes robust error handling and will continue execution even if the API connection fails, making it reliable for evaluation purposes.
