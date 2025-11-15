import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db

# Set up logging
logging.basicConfig(
    filename="log/get_vendors_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    """
    This function merges different tables to generate an overall vendor summary,
    adding new columns in the resultant DataFrame.
    """
    try:
        query = """
        WITH FreightSummary AS (
            SELECT 
                VendorNumber, 
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),
        PurchaseSummary AS (
            SELECT 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Volume,
                pp.Price AS ActualPrice, 
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY 
                p.VendorNumber, p.VendorName, p.Brand, p.Description,
                p.PurchasePrice, pp.Price, pp.Volume
        ),
        SalesSummary AS (
            SELECT
                VendorNo,
                Brand,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollar,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )
        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.ActualPrice,
            ps.PurchasePrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollar,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
        """

        vendor_sales_summary = pd.read_sql_query(query, conn)
        logging.info("Vendor summary successfully created.")
        return vendor_sales_summary

    except Exception as e:
        logging.error(f"Error creating vendor summary: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure
    
def clean_data(df):
    '''this function will clean the data'''
    #changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    #filling missing values with 0
    df.fillna(0,inplace=True)

    #removing spaces from Categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #creating new columns for Betteer analysis
    df['GrossProfit'] = df['TotalSalesDollar'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollar'])*100
    df['StockTurnover'] = (df['TotalSalesQuantity']/df['TotalPurchaseQuantity'])*100
    df['SalestoPurchaseRatio'] = (df['TotalSalesDollar']/df['TotalPurchaseDollars'])

    return df

if __name__ == '__main__':
    #creating Database connection
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table...')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data....')
    ingest_db(clean_df,'vendor_sales_summary',conn)
    logging.info('Completed')