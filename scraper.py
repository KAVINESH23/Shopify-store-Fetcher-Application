import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import extract_emails_phones, extract_social_links, extract_faqs

def scrape_shopify_store(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, 'lxml')

        brand_context = {
            "store_url": url,
            "hero_products": [],
            "all_products": [],
            "privacy_policy": "",
            "refund_policy": "",
            "faqs": [],
            "social_links": {},
            "contact_details": {},
            "about_brand": "",
            "important_links": {}
        }

        # Hero products - common on homepage
        for product in soup.select('a[href*="/products/"]')[:10]:
            brand_context["hero_products"].append({
                "title": product.get_text(strip=True),
                "url": urljoin(url, product.get("href"))
            })

        # Product catalog (pagination possible via /collections/all)
        try:
            all_collection_url = urljoin(url, "/collections/all")
            r = session.get(all_collection_url, headers=headers)
            soup_all = BeautifulSoup(r.content, 'lxml')
            for prod in soup_all.select('a[href*="/products/"]'):
                title = prod.get_text(strip=True)
                href = urljoin(all_collection_url, prod.get("href"))
                if title and href not in [p["url"] for p in brand_context["all_products"]]:
                    brand_context["all_products"].append({"title": title, "url": href})
        except:
            pass

        # Policies and About
        for link in soup.find_all("a", href=True):
            href = link["href"].lower()
            text = link.get_text(strip=True)
            if "privacy" in href:
                brand_context["privacy_policy"] = urljoin(url, link["href"])
            elif "refund" in href or "return" in href:
                brand_context["refund_policy"] = urljoin(url, link["href"])
            elif "about" in href:
                brand_context["about_brand"] = urljoin(url, link["href"])
            elif "contact" in href:
                brand_context["important_links"]["contact_us"] = urljoin(url, link["href"])
            elif "blog" in href:
                brand_context["important_links"]["blog"] = urljoin(url, link["href"])
            elif "track" in href:
                brand_context["important_links"]["order_tracking"] = urljoin(url, link["href"])

        # Extract emails and phones
        brand_context["contact_details"] = extract_emails_phones(response.text)

        # Extract social media
        brand_context["social_links"] = extract_social_links(response.text)

        # Try to extract FAQs
        brand_context["faqs"] = extract_faqs(soup)

        return brand_context

    except Exception as e:
        raise RuntimeError(f"Failed to scrape: {e}")
