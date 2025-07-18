import re
from bs4 import BeautifulSoup

def extract_emails_phones(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"\+?\d[\d -]{8,}\d", text)
    return {
        "emails": list(set(emails)),
        "phones": list(set(phones))
    }

def extract_social_links(html):
    social = {}
    platforms = ["facebook", "instagram", "tiktok", "twitter", "youtube", "linkedin"]
    for platform in platforms:
        match = re.search(rf'https?://(?:www\.)?{platform}\.com/[^\s"\']+', html, re.IGNORECASE)
        if match:
            social[platform] = match.group(0)
    return social

def extract_faqs(soup):
    faqs = []
    questions = soup.find_all(['h2', 'h3', 'strong'])
    for q in questions:
        question_text = q.get_text(strip=True).lower()
        if "?" in question_text:
            answer_tag = q.find_next_sibling(["p", "div"])
            answer = answer_tag.get_text(strip=True) if answer_tag else ""
            faqs.append({"question": question_text, "answer": answer})
    return faqs
