# Inventory & Vendor Performance Analysis  
### End-to-End Data Engineering & Analytics Project (Python, SQL, Power BI)

This project focuses on analyzing inventory movement, vendor performance, purchase trends, and stock discrepancies using Python, SQLite, and Power BI.  
It showcases real-world skills in data ingestion, cleaning, SQL analysis, automation, and dashboard creation.

---

## 📌 Project Objectives

- Build an end-to-end data pipeline for inventory and vendor datasets.
- Clean and ingest multi-million row CSV files into a SQLite database.
- Perform EDA to understand purchase patterns and vendor efficiency.
- Create SQL queries for vendor scorecards, stock variance, and pricing summaries.
- Build interactive Power BI dashboards visualizing key business KPIs.

## 📁 Project Structure

```
project/
│
├── scripts/
│   ├── ingestion_db.py
│   ├── get_vendors_summary.py
│
├── notebooks/
│   ├── Exploratory_data_analysis.ipynb
│   ├── Vendor Performance Analysis.ipynb
│
├── Data/                  # Raw CSVs (ignored)
├── log/                   # Logging folder
├── .gitignore
└── README.md
```


## 🛠️ **Tech Stack Used**

### **Programming & Tools**
- Python (Pandas, SQLite3, Logging)
- Jupyter Notebook
- SQL (SQLite)
- Power BI  
- Visual Studio Code  
- Git & GitHub

---

## 🚀 **End-to-End Workflow**

### **1. Data Ingestion**
- Wrote Python scripts to load large datasets into SQLite:
  - Purchases (2.3M+ rows)
  - Sales (12M+ rows)
  - Inventory files (200K+ rows)
  - Vendor invoices

- Used chunked loading to handle 300MB+ CSV files without memory errors.

### **2. Data Cleaning**
- Removed duplicates  
- Handled missing values  
- Standardized date formats  
- Normalized schemas between different datasets  

### **3. Exploratory Data Analysis**
Performed in Jupyter Notebooks:
- Vendor purchase frequency
- Item-wise purchase trends
- Price variations across vendors
- Stock discrepancies (begin vs end inventory)

### **4. SQL Analysis**
Created SQL queries for:
- Vendor performance summary  
- Inventory variance  
- Purchase price comparison  
- High-volume & low-volume vendors  
- Product-level profitability insights  

### **5. Power BI Dashboard**
Designed visualizations for:
- Vendor scorecards  
- Purchase cycle trends  
- Inventory balance comparison  
- Top contributing vendors  
- Item-level demand and supply  

---

## 💡 Key Insights Delivered

- Identified vendors with high delay rates & inconsistent pricing.  
- Highlighted items with negative stock variance indicating mismatch.  
- Detected seasonal purchase trends based on sales and movement data.  
- Found top contributors to purchase costs and revenue.

---

## 🧩 Challenges Faced & Solutions

### **Large CSVs (300MB–1.5GB)**
- Solved using chunk-based loading and batched inserts.

### **Slow SQL queries**
- Added indexes on `vendor_id`, `item_id`, and `date` fields to improve speed.

### **GitHub rejecting large files**
- Added `.gitignore` to exclude CSV & DB files from repository.

---

## 📊 Dashboard Preview
(*Add screenshots of your Power BI dashboard here once created*)

---

## 📎 How to Run the Project

### **1. Clone the Repository**

### **2. Install Python Dependencies**

### **3. Run the Data Ingestion Script**

### **4. Open Notebooks**
Use Jupyter Notebook or VS Code to explore the EDA and vendor analysis.

---

## 📬 Contact

**Nitin Chimmalagi**  
Data Analyst | Python | SQL | Power BI  
GitHub: NitinChimmalagi  

---
