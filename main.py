"""
University Library LangGraph Hello World
Routes between Undergraduate and Graduate support based on user queries
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
import typing

# Initialize Ollama with Llama 3.3
# Use host.docker.internal for Docker environments on macOS
import os
ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
llm = OllamaLLM(model="llama3.3", base_url=ollama_base_url)

# Define the state structure
class LibraryState(TypedDict):
    user_query: str
    support_level: str
    response: str
    routing_reason: str

def classify_support_level(state: LibraryState) -> LibraryState:
    """
    Determines whether the query needs undergraduate or graduate level support
    """
    query = state["user_query"].lower()
    
    # Graduate-level indicators
    graduate_keywords = [
        "thesis", "dissertation", "phd", "graduate", "masters", "research methodology",
        "literature review", "systematic review", "meta-analysis", "peer review",
        "academic publishing", "conference presentation", "grant writing", 
        "statistical analysis", "qualitative research", "quantitative research",
        "theoretical framework", "methodology", "advanced", "specialized database"
    ]
    
    # Undergraduate-level indicators
    undergraduate_keywords = [
        "homework", "assignment", "undergraduate", "freshman", "sophomore", 
        "junior", "senior", "basic", "introduction", "how to cite", "mla", "apa",
        "first time", "beginner", "simple", "easy", "quick", "basic research",
        "class project", "term paper", "book report", "study guide"
    ]
    
    # Check for graduate indicators
    graduate_score = sum(1 for keyword in graduate_keywords if keyword in query)
    undergraduate_score = sum(1 for keyword in undergraduate_keywords if keyword in query)
    
    # Default routing logic
    if graduate_score > undergraduate_score:
        support_level = "graduate"
        reason = f"Detected {graduate_score} graduate-level indicators"
    elif undergraduate_score > graduate_score:
        support_level = "undergraduate" 
        reason = f"Detected {undergraduate_score} undergraduate-level indicators"
    else:
        # Default heuristics for ambiguous cases
        if any(word in query for word in ["advanced", "complex", "comprehensive", "in-depth"]):
            support_level = "graduate"
            reason = "Complexity indicators suggest graduate level"
        elif any(word in query for word in ["help", "how", "what", "where", "basic"]):
            support_level = "undergraduate"
            reason = "Question structure suggests undergraduate level"
        else:
            support_level = "undergraduate"  # Default to undergraduate
            reason = "No clear indicators, defaulting to undergraduate"
    
    state["support_level"] = support_level
    state["routing_reason"] = reason
    return state

def undergraduate_support(state: LibraryState) -> LibraryState:
    """
    Provides undergraduate-level library support
    """
    prompt = f"""
    You are a friendly university librarian helping an undergraduate student. 
    Provide clear, accessible guidance that assumes basic familiarity with library resources.
    Focus on:
    - Step-by-step instructions
    - Basic research skills
    - Common undergraduate resources
    - Encouraging and supportive tone
    - Practical, actionable advice
    
    Student question: {state['user_query']}
    
    Provide a helpful response:
    """
    
    response = llm.invoke(prompt)
    state["response"] = f"[UNDERGRADUATE SUPPORT]\n{response}"
    return state

def graduate_support(state: LibraryState) -> LibraryState:
    """
    Provides graduate-level library support
    """
    prompt = f"""
    You are a specialized research librarian supporting graduate students and researchers.
    Provide sophisticated guidance that assumes advanced research experience.
    Focus on:
    - Advanced research methodologies
    - Specialized databases and resources
    - Academic writing and publishing
    - Research efficiency and depth
    - Professional academic tone
    - Cutting-edge tools and techniques
    
    Research question: {state['user_query']}
    
    Provide expert guidance:
    """
    
    response = llm.invoke(prompt)
    state["response"] = f"[GRADUATE SUPPORT]\n{response}"
    return state

def route_support(state: LibraryState) -> Literal["undergraduate", "graduate"]:
    """
    Routes to appropriate support level based on classification
    """
    return typing.cast(Literal["undergraduate", "graduate"], state["support_level"])

# Build the graph
def create_library_graph():
    workflow = StateGraph(LibraryState)
    
    # Add nodes
    workflow.add_node("classifier", classify_support_level)
    workflow.add_node("undergraduate", undergraduate_support)
    workflow.add_node("graduate", graduate_support)
    
    # Add edges
    workflow.set_entry_point("classifier")
    workflow.add_conditional_edges(
        "classifier",
        route_support,
        {
            "undergraduate": "undergraduate",
            "graduate": "graduate"
        }
    )
    workflow.add_edge("undergraduate", END)
    workflow.add_edge("graduate", END)
    
    return workflow.compile()

def get_library_assistant_response(user_query: str) -> dict:
    """
    Entry point for web/API: runs the graph and returns the result dict.
    """
    app = create_library_graph()
    initial_state = {
        "user_query": user_query,
        "support_level": "",
        "response": "",
        "routing_reason": ""
    }
    result = app.invoke(initial_state)
    return result

def main():
    """
    Main function to run the library assistant
    """
    app = create_library_graph()
    
    print("🏛️  University Library Assistant (LangGraph + Llama 3.3)")
    print("=" * 60)
    print("Ask me anything about library resources and research!")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("📚 Your question: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thanks for using the Library Assistant! 📖")
            break
            
        if not user_input:
            continue
            
        # Run the graph
        try:
            initial_state = {
                "user_query": user_input,
                "support_level": "",
                "response": "",
                "routing_reason": ""
            }
            
            result = app.invoke(initial_state)
            
            print(f"\n🎯 Routing: {result['support_level'].upper()} support")
            print(f"💭 Reason: {result['routing_reason']}")
            print(f"\n{result['response']}")
            print("\n" + "="*60 + "\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()