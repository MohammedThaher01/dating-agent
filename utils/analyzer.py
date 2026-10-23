import json
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(temperature=0.2, model_name="openai/gpt-oss-120b")

class ProfileAnalysis(BaseModel):
    needs: list[str] = Field(description="3 deep psychological or lifestyle needs derived from their online presence.")
    hobbies: list[str] = Field(description="3 concrete hobbies they engage in.")
    interests: list[str] = Field(description="3 broader topics or fields they are interested in.")
    qualities: list[str] = Field(description="3 personality traits or other notable qualities found.")

def analyze_person(linkedin_data: dict, instagram_data: dict) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert psychological profiler. You receive raw LinkedIn and Instagram data. You must analyze the person and extract their needs, hobbies, interests, and other qualities."),
        ("user", "LinkedIn Data: {li_data}\n\nInstagram Data: {ig_data}\n\nAnalyze this person and output the structured JSON.")
    ])
    
    chain = prompt | llm.with_structured_output(ProfileAnalysis)
    result = chain.invoke({"li_data": json.dumps(linkedin_data), "ig_data": json.dumps(instagram_data)})
    
    return result.dict()