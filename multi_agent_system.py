"""
Multi-Agent Travel Planner System
==================================
Built with LangChain + LangGraph + Google Gemini

Agents:
1. 🗺️  DestinationResearchAgent  – Researches destination info, weather, visa requirements
2. ��  ItineraryPlannerAgent      – Builds a day-by-day itinerary
3. 💰  BudgetEstimatorAgent       – Estimates costs (flights, hotels, food, activities)
4. 📋  TravelSummaryAgent         – Compiles everything into a final travel plan

Workflow (LangGraph):
  START → destination_research → itinerary_planner → budget_estimator → travel_summary → END
"""

from typing import TypedDict, Annotated
import time
import os
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# 1. SHARED STATE  (passed between all agents)
# ─────────────────────────────────────────────
class TravelState(TypedDict):
    user_request: str
    destination_info: str
    itinerary: str
    budget_estimate: str
    final_plan: str
    messages: Annotated[list[BaseMessage], add_messages]


# ─────────────────────────────────────────────
# 2. LLM  (Gemini, OpenAI, or OpenRouter)
# ─────────────────────────────────────────────
# Load API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure which LLM provider to use
USE_OPENROUTER = True  # Set to True to use OpenRouter
USE_OPENAI = False  # Set to True to use OpenAI (leave both False for Gemini)

def get_llm():
    """Initialize and return the configured LLM."""
    if USE_OPENROUTER:
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please check your .env file.")
        return ChatOpenAI(
            model="openai/gpt-4o-mini",  # OpenRouter model format
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",  # Optional
                "X-Title": "Multi-Agent Travel Planner"  # Optional
            }
        )
    elif USE_OPENAI:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
        return ChatOpenAI(
            model="gpt-4o-mini",  # Cost-effective model
            api_key=OPENAI_API_KEY,
            temperature=0.7
        )
    else:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )


def call_llm_with_retry(llm, messages, max_retries=5, initial_delay=70):
    """Call LLM with exponential backoff retry logic for rate limits."""
    for attempt in range(max_retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                if attempt < max_retries - 1:
                    # Extract retry delay from error message if available
                    import re
                    retry_match = re.search(r'retry in (\d+(?:\.\d+)?)', error_str)
                    if retry_match:
                        delay = float(retry_match.group(1)) + 5  # Add 5s buffer
                    else:
                        delay = initial_delay * (2 ** attempt)
                    
                    print(f"⏳ Rate limit hit. Waiting {int(delay)}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(delay)
                else:
                    print("❌ Max retries reached. Your Gemini quota is exhausted.")
                    print("💡 Options:")
                    print("   1. Wait until tomorrow for quota reset")
                    print("   2. Set USE_OPENAI = True in the code to use OpenAI")
                    print("   3. Upgrade your Gemini API plan")
                    raise
            else:
                raise


# ─────────────────────────────────────────────
# 3. AGENT NODES
# ─────────────────────────────────────────────

def destination_research_agent(state: TravelState) -> dict:
    """
    Agent 1 - DestinationResearchAgent
    Role: Research the destination - highlights, best time to visit,
          visa requirements, and local tips.
    """
    llm = get_llm()
    prompt = f"""You are a knowledgeable travel researcher.
The user wants to travel with these details:
{state['user_request']}

Provide a concise research report covering:
1. Top highlights / must-see attractions
2. Best time to visit & weather
3. Visa / entry requirements (for Indian passport holders unless specified)
4. Local customs & safety tips
5. Getting around (transport options)

Be specific and practical. Keep it under 350 words."""

    response = call_llm_with_retry(llm, [HumanMessage(content=prompt)])
    destination_info = response.content

    print("\n🗺  [DestinationResearchAgent] Done.\n")
    time.sleep(20)  # Rate limiting delay between agents
    return {
        "destination_info": destination_info,
        "messages": [AIMessage(content=destination_info, name="DestinationResearchAgent")]
    }


def itinerary_planner_agent(state: TravelState) -> dict:
    """
    Agent 2 - ItineraryPlannerAgent
    Role: Build a detailed day-by-day itinerary using the destination research.
    """
    llm = get_llm()
    prompt = f"""You are an expert travel itinerary planner.

User's travel request:
{state['user_request']}

Destination research provided by the research agent:
{state['destination_info']}

Create a detailed day-by-day itinerary. For each day include:
- Morning, afternoon, and evening activities
- Specific places to visit with brief descriptions
- Meal suggestions (local dishes / restaurants)
- Estimated travel time between spots

Make the itinerary practical, balanced (not rushed), and exciting.
Keep it under 500 words."""

    response = call_llm_with_retry(llm, [HumanMessage(content=prompt)])
    itinerary = response.content

    print("🗓️  [ItineraryPlannerAgent] Done.\n")
    time.sleep(20)  # Rate limiting delay between agents
    return {
        "itinerary": itinerary,
        "messages": [AIMessage(content=itinerary, name="ItineraryPlannerAgent")]
    }


def budget_estimator_agent(state: TravelState) -> dict:
    """
    Agent 3 - BudgetEstimatorAgent
    Role: Estimate the overall trip budget based on the itinerary.
    """
    llm = get_llm()
    prompt = f"""You are a travel budget analyst.

User's travel request:
{state['user_request']}

Planned itinerary:
{state['itinerary']}

Provide a realistic budget estimate in USD covering:
1. Flights (round-trip, economy)
2. Accommodation (per night x number of nights)
3. Daily food & drinks
4. Activities / entrance fees mentioned in the itinerary
5. Local transport
6. Miscellaneous (SIM card, souvenirs, tips)

Present as a clear table, then give a TOTAL for budget / mid-range / luxury tiers.
Keep it under 300 words."""

    response = call_llm_with_retry(llm, [HumanMessage(content=prompt)])
    budget_estimate = response.content

    print("💰 [BudgetEstimatorAgent] Done.\n")
    time.sleep(20)  # Rate limiting delay between agents
    return {
        "budget_estimate": budget_estimate,
        "messages": [AIMessage(content=budget_estimate, name="BudgetEstimatorAgent")]
    }


def travel_summary_agent(state: TravelState) -> dict:
    """
    Agent 4 - TravelSummaryAgent
    Role: Compile all agent outputs into a polished, readable final travel plan.
    """
    llm = get_llm()
    prompt = f"""You are a professional travel consultant creating a final trip report.

Compile the following information into a well-structured, engaging travel plan document.

USER REQUEST:
{state['user_request']}

DESTINATION RESEARCH:
{state['destination_info']}

ITINERARY:
{state['itinerary']}

BUDGET ESTIMATE:
{state['budget_estimate']}

Format the final plan with clear sections:
TRIP OVERVIEW
DESTINATION INSIGHTS
DAY-BY-DAY ITINERARY
BUDGET BREAKDOWN
PRO TIPS & REMINDERS

Make it feel like a premium travel guide the user would want to print and carry.
Be concise but complete."""

    response = call_llm_with_retry(llm, [HumanMessage(content=prompt)])
    final_plan = response.content

    print("📋 [TravelSummaryAgent] Done.\n")
    return {
        "final_plan": final_plan,
        "messages": [AIMessage(content=final_plan, name="TravelSummaryAgent")]
    }


# ─────────────────────────────────────────────
# 4. BUILD THE LANGGRAPH WORKFLOW
# ─────────────────────────────────────────────

def build_graph():
    """
    Define nodes and edges for the multi-agent workflow.

    Flow:
      START
        |
        v
      destination_research   <-- Agent 1
        |
        v
      itinerary_planner      <-- Agent 2 (uses Agent 1's output)
        |
        v
      budget_estimator       <-- Agent 3 (uses Agent 2's output)
        |
        v
      travel_summary         <-- Agent 4 (compiles everything)
        |
        v
      END
    """
    graph = StateGraph(TravelState)

    graph.add_node("destination_research", destination_research_agent)
    graph.add_node("itinerary_planner",    itinerary_planner_agent)
    graph.add_node("budget_estimator",     budget_estimator_agent)
    graph.add_node("travel_summary",       travel_summary_agent)

    graph.add_edge(START,                  "destination_research")
    graph.add_edge("destination_research", "itinerary_planner")
    graph.add_edge("itinerary_planner",    "budget_estimator")
    graph.add_edge("budget_estimator",     "travel_summary")
    graph.add_edge("travel_summary",       END)

    return graph.compile()


# ─────────────────────────────────────────────
# 5. MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   Multi-Agent Travel Planner  (LangGraph + Gemini)")
    print("=" * 60)
    print("\nAgents in this system:")
    print("  1. DestinationResearchAgent")
    print("  2. ItineraryPlannerAgent")
    print("  3. BudgetEstimatorAgent")
    print("  4. TravelSummaryAgent")
    print("\nAll agents collaborate through a shared LangGraph state.\n")
    print("-" * 60)

    # Dynamic user input
    destination = input("Where do you want to travel? (e.g., Tokyo, Japan): ").strip()
    duration    = input("How many days? (e.g., 7): ").strip()
    travelers   = input("Number of travelers? (e.g., 2): ").strip()
    interests   = input("Your interests? (e.g., culture, food, adventure): ").strip()
    budget_pref = input("Budget preference? (budget / mid-range / luxury): ").strip()

    user_request = (
        f"Destination: {destination}\n"
        f"Duration: {duration} days\n"
        f"Travelers: {travelers}\n"
        f"Interests: {interests}\n"
        f"Budget preference: {budget_pref}"
    )

    print("\n" + "=" * 60)
    print("Starting multi-agent workflow...\n")

    app = build_graph()

    initial_state: TravelState = {
        "user_request":     user_request,
        "destination_info": "",
        "itinerary":        "",
        "budget_estimate":  "",
        "final_plan":       "",
        "messages":         [],
    }

    final_state = app.invoke(initial_state)

    print("=" * 60)
    print("           YOUR COMPLETE TRAVEL PLAN")
    print("=" * 60)
    print(final_state["final_plan"])
    print("\n" + "=" * 60)

    save = input("\nSave the plan to travel_plan.txt? (y/n): ").strip().lower()
    if save == "y":
        with open("travel_plan.txt", "w", encoding="utf-8") as f:
            f.write(f"TRAVEL PLAN\n{'='*60}\n\n")
            f.write(f"Request:\n{user_request}\n\n{'='*60}\n\n")
            f.write(final_state["final_plan"])
        print("Saved to travel_plan.txt")


if __name__ == "__main__":
    main()