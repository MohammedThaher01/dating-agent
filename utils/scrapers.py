import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

def scrape_with_retry(endpoint: str, payload: dict, retries: int = 3, timeout: int = 120) -> dict:
    for attempt in range(retries):
        try:
            response = requests.post(endpoint, json=payload, timeout=timeout)
            if response.status_code in [200, 201]:
                return response.json()
            print(f"Error {response.status_code}: {response.text}")
            return None
        except requests.exceptions.ReadTimeout:
            print(f"Timeout on attempt {attempt + 1}/{retries}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Exception: {e}")
            return None
    return None

def scrape_linkedin(profile_url: str) -> dict:
    if not APIFY_API_TOKEN:
        return {"error": "No API key"}
        
    endpoint = f"https://api.apify.com/v2/acts/vulnv~linkedin-profile-scraper/run-sync-get-dataset-items?token={APIFY_API_TOKEN}"
    data = scrape_with_retry(endpoint, {"urls": [profile_url]})
    
    if data and isinstance(data, list) and len(data) > 0:
        user_data = data[0]
        experiences = user_data.get("experience") or []
        summary = user_data.get("about") or user_data.get("summary") or ""
        return {
            "headline": user_data.get("headline") or "",
            "summary": summary,
            "experiences": experiences[:3]
        }
    return {"error": "Failed to fetch LinkedIn profile"}

def scrape_instagram(profile_url: str) -> dict:
    if not APIFY_API_TOKEN:
        return {"error": "No API key"}
        
    endpoint = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={APIFY_API_TOKEN}"
    data = scrape_with_retry(endpoint, {"directUrls": [profile_url], "resultsType": "details"})
    
    if data and isinstance(data, list) and len(data) > 0:
        user_data = data[0]
        latest_posts = user_data.get("latestPosts") or []
        return {
            "biography": user_data.get("biography") or "",
            "followers": user_data.get("followersCount") or 0,
            "recent_posts": [post.get("caption") for post in latest_posts[:5] if isinstance(post, dict) and post.get("caption")]
        }
    return {"error": "Failed to fetch Instagram profile"}