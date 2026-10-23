from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.scrapers import scrape_linkedin, scrape_instagram
from utils.analyzer import analyze_person
from engine import app as dating_engine

app = FastAPI(title="Agentic Dating API")

class ProfileUrls(BaseModel):
    name: str
    linkedin_url: str
    instagram_url: str

@app.post("/api/extract-profile")
def extract_profile(user: ProfileUrls):
    li_data = scrape_linkedin(user.linkedin_url)
    ig_data = scrape_instagram(user.instagram_url)
    
    if "error" in li_data and "error" in ig_data:
        raise HTTPException(status_code=400, detail="Could not retrieve data from either source.")
        
    analysis = analyze_person(li_data, ig_data)
    
    return {
        "status": "success",
        "name": user.name,
        "profile_page": analysis 
    }