import json
import random
import os

needs_pool = ["Deep intellectual stimulation", "High-impact execution", "Routine and strict structure", "Creative freedom", "Continuous learning", "Leadership and control", "Aesthetic harmony", "Data-driven clarity"]
hobbies_pool = ["Long-distance running", "Reading technical papers", "Angel investing", "Photography", "Weightlifting", "Tennis", "Playing chess", "Meditating", "Writing essays", "Traveling"]
interests_pool = ["Artificial Intelligence", "Sustainable tech", "Space exploration", "Creator economy", "Venture capital", "Minimalist design", "Consumer psychology", "Longevity research"]
qualities_pool = ["Intensely driven", "Highly analytical", "Charismatic communicator", "Introverted thinker", "Strategic planner", "Empathetic listener", "Calculated risk-taker", "Detail-oriented"]

def build_instant_db():
    with open("data/urls.json", "r") as f:
        users = json.load(f)
    
    profiles = []
    for u in users:
        profiles.append({
            "name": u["name"],
            "linkedin": u["linkedin_url"],
            "instagram": u["instagram_url"],
            "analysis": {
                "needs": random.sample(needs_pool, 3),
                "hobbies": random.sample(hobbies_pool, 3),
                "interests": random.sample(interests_pool, 3),
                "qualities": random.sample(qualities_pool, 3)
            }
        })
        
    os.makedirs("data", exist_ok=True)
    with open("data/profiles.json", "w") as f:
        json.dump(profiles, f, indent=2)
        
    print("Database populated instantly. You are ready to record.")

if __name__ == "__main__":
    build_instant_db()