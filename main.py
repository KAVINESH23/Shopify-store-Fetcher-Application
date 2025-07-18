from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_shopify_store

app = FastAPI()

class URLRequest(BaseModel):
    website_url: str

@app.post("/extract-brand-context")
async def extract_brand_context(request: URLRequest):
    try:
        data = scrape_shopify_store(request.website_url)
        if not data:
            raise HTTPException(status_code=401, detail="Website not accessible or not aalid Shopify site.")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
