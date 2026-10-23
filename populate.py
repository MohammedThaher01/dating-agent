import json
import os
from utils.scrapers import scrape_linkedin, scrape_instagram
from utils.analyzer import analyze_person

def populate_database():
    with open("data/urls.json", "r") as f:
        users = json.load(f)
    
    profiles = []
    os.makedirs("data", exist_ok=True)
    
    # Load existing profiles to avoid re-scraping
    if os.path.exists("data/profiles.json"):
        with open("data/profiles.json", "r") as f:
            profiles = json.load(f)
            
    completed_names = {p["name"] for p in profiles}
    
    for i, user in enumerate(users):
        if user["name"] in completed_names:
            print(f"Skipping {i+1}/25: {user['name']} (Already completed)")
            continue
            
        print(f"Processing {i+1}/25: {user['name']}...")
        try:
            li_data = scrape_linkedin(user['linkedin_url'])
            ig_data = scrape_instagram(user['instagram_url'])
            
            if "error" in li_data and "error" in ig_data:
                print(f"Failed to scrape {user['name']}")
                continue
                
            analysis = analyze_person(li_data, ig_data)
            profiles.append({
                "name": user['name'],
                "linkedin": user['linkedin_url'],
                "instagram": user['instagram_url'],
                "analysis": analysis
            })
            
            # Save incrementally after every successful person
            with open("data/profiles.json", "w") as f:
                json.dump(profiles, f, indent=2)
                
        except Exception as e:
            print(f"Error processing {user['name']}: {e}")
            
    print("Database populated successfully.")

if __name__ == "__main__":
    populate_database()