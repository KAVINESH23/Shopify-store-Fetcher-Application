# SHOPIFY STORE APPLICATION
# OVERVIEW
A Python-based web scraping application that extracts product and brand-related insights from a Shopify-based store URL (without using the Shopify API). It identifies competitor websites via a simple Google search and scrapes similar data from them as well. All extracted data is persisted into a local SQLite3 database.

# PURPOSE
The primary goal is to extract structured, brand-specific eCommerce data (products, policies, FAQs, contact info, social handles) from a Shopify store and its competitors using lightweight scraping methods and Google-based discovery. This tool helps in competitive analysis, market research, and brand comparison without relying on paid APIs.

# TECH STACK
Python - Core logic & scraping
FastAPI - REST API backend to trigger scraping
BeautifulSoup & Requests - For HTML parsing and scraping
Postman - For the testing the backend

# ENDPOINTS
## Extract Brand Data
http://127.0.0.1:8000/extract-brand-context

POST /extract-brand-content

{
  "website_url": "https://lucyandyak.com"
}
