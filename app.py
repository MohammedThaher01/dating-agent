import streamlit as st
import json
import time
from utils.scrapers import scrape_linkedin, scrape_instagram
from utils.analyzer import analyze_person
from engine import app as dating_engine

st.set_page_config(layout="wide", page_title="Agentic Matchmaker")

# Load pre-computed database
@st.cache_data
def load_db():
    try:
        with open("data/profiles.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

db_profiles = load_db()

st.title("Agentic Matchmaker")

# Step 1: Paste Links
st.sidebar.header("Add New Person")
new_name = st.sidebar.text_input("Name")
new_li = st.sidebar.text_input("LinkedIn URL")
new_ig = st.sidebar.text_input("Instagram URL")

if st.sidebar.button("Analyze & Date"):
    with st.spinner(f"Agent is reading {new_name}'s profiles..."):
        li_data = scrape_linkedin(new_li)
        ig_data = scrape_instagram(new_ig)
        new_profile_analysis = analyze_person(li_data, ig_data)
        
        st.session_state["target_user"] = {
            "name": new_name,
            "analysis": new_profile_analysis
        }

if "target_user" in st.session_state:
    target = st.session_state["target_user"]
    
    # Step 2: The Profile Page
    st.header(f"Profile Page: {target['name']}")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Needs:**\n- " + "\n- ".join(target['analysis']['needs']))
    col2.markdown(f"**Hobbies:**\n- " + "\n- ".join(target['analysis']['hobbies']))
    col3.markdown(f"**Interests:**\n- " + "\n- ".join(target['analysis']['interests']))
    
    st.divider()
    
    # Step 3: The Agents Date
    st.header("Live Date Simulation")
    match_candidate = db_profiles[0] # Pick the first person in DB for the live demo
    
    st.write(f"**{target['name']}'s Agent** is now dating **{match_candidate['name']}'s Agent**...")
    
    date_container_a, date_container_msg, date_container_b = st.columns([1, 2, 1])
    date_container_a.subheader(f"{target['name']}'s Thoughts")
    date_container_msg.subheader("Conversation")
    date_container_b.subheader(f"{match_candidate['name']}'s Thoughts")
    
    initial_state = {
        "turn_count": 0, "max_turns": 2, "history": [],
        "agent_a_profile": target['analysis'], "agent_b_profile": match_candidate['analysis']
    }
    
    final_score = 50
    for output in dating_engine.stream(initial_state):
        for node_name, state in output.items():
            latest_msg = state["history"][-1]
            if latest_msg["speaker"] == "Agent A":
                date_container_a.info(latest_msg["thought"])
                date_container_msg.markdown(f"**{target['name']}:** {latest_msg['message']}")
            else:
                date_container_b.warning(latest_msg["thought"])
                date_container_msg.markdown(f"**{match_candidate['name']}:** {latest_msg['message']}")
            final_score = latest_msg.get("score", final_score)
            time.sleep(1) # Slow down slightly for video effect
            
    st.divider()
    
    # Step 4: Final Rankings
    st.header("Final Rankings")
    st.write(f"Ranking who fits {target['name']} best across the 25-person database...")
    
    # Mocking the rest of the 24 scores for immediate UI rendering in the video
    import random
    rankings = [{"Name": match_candidate['name'], "Compatibility": final_score}]
    for p in db_profiles[1:]:
        rankings.append({"Name": p['name'], "Compatibility": random.randint(40, 95)})
        
    rankings = sorted(rankings, key=lambda x: x["Compatibility"], reverse=True)
    st.dataframe(rankings, use_container_width=True)