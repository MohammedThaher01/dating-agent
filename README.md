# Agentic Matchmaker

An autonomous matchmaking platform where LLM agents extract traits from public LinkedIn and Instagram profiles, simulate virtual dates to evaluate compatibility, and rank optimal partner fits. 

### How It Works
1. **Extraction:** Walled-garden data is parsed via Apify to guarantee instant, structured JSON payloads.
2. **Analysis:** Llama-3 evaluates psychological alignment and extracts deep needs, hobbies, and interests.
3. **Simulation:** Agents use a two-step generation loop per turn, outputting hidden 'internal thoughts' before generating their spoken dialogue to simulate genuine strategic dating.

### Tech Stack
* Python / FastAPI
* Streamlit
* LangGraph / LangChain
* Groq (Llama-3 70b)
* Apify