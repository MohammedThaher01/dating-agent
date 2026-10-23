from typing import TypedDict, List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(temperature=0.7, model_name="openai/gpt-oss-20b")

class DateState(TypedDict):
    turn_count: int
    max_turns: int
    history: List[dict]
    agent_a_profile: dict
    agent_b_profile: dict

class AgentTurn(BaseModel):
    internal_thought: str = Field(description="The agent's private psychoanalysis of the other person based on their profiles.")
    spoken_message: str = Field(description="The actual dialogue spoken to the other agent.")
    compatibility_score: int = Field(description="Current score 0-100", default=50)

def generate_turn(agent_profile, other_profile, history):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are dating on behalf of your human. Your human's profile: {agent_profile}. The person you are dating: {other_profile}. Analyze their traits ruthlessly. You are currently on a virtual date."),
        ("user", "Conversation history: {history}\n\nGenerate your next response, including your hidden internal thoughts about their last message and what you will say next.")
    ])
    chain = prompt | llm.with_structured_output(AgentTurn)
    return chain.invoke({"agent_profile": agent_profile, "other_profile": other_profile, "history": history})

def agent_a_node(state: DateState):
    response = generate_turn(state["agent_a_profile"], state["agent_b_profile"], state["history"])
    state["history"].append({"speaker": "Agent A", "thought": response.internal_thought, "message": response.spoken_message, "score": response.compatibility_score})
    state["turn_count"] += 1
    return state

def agent_b_node(state: DateState):
    response = generate_turn(state["agent_b_profile"], state["agent_a_profile"], state["history"])
    state["history"].append({"speaker": "Agent B", "thought": response.internal_thought, "message": response.spoken_message, "score": response.compatibility_score})
    return state

def check_end(state: DateState):
    if state["turn_count"] >= state["max_turns"]:
        return END
    return "agent_b"

workflow = StateGraph(DateState)
workflow.add_node("agent_a", agent_a_node)
workflow.add_node("agent_b", agent_b_node)
workflow.set_entry_point("agent_a")
workflow.add_conditional_edges("agent_a", check_end)
workflow.add_edge("agent_b", "agent_a")
app = workflow.compile()