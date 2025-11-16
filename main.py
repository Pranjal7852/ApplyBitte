import os
from dotenv import load_dotenv
from graph import build_graph
from state import AppState, ExperienceItem, Profile

load_dotenv()

# Check if Ollama is accessible
def check_ollama():
    try:
        from langchain_ollama import OllamaLLM
        model = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
        print(f"Checking Ollama connection (model: {model})...")
        llm = OllamaLLM(model=model)
        # Try a simple test
        test_response = llm.invoke("Say 'OK' if you can hear me.")
        print(f"✓ Ollama is accessible. Test response: {test_response[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("Make sure Ollama is running and the model is available.")
        print("You can start Ollama with: ollama serve")
        print("And pull a model with: ollama pull gpt-oss:20b")
        return False

def example_profile():
    e1 = ExperienceItem(company="BMW", role="AI Engineer", dates="2024-2025", highlights=["Built agentic AI systems for plastic recycling", "Worked with LLMs and CrewAI"])
    p = Profile(name="Pranjal Goel", title="Full Stack Engineer", experience=[e1], skills={"languages": ["TypeScript", "Python"], "ai": ["LLMs"]}, achievements=["GSoC contributor"], education=["TUM program"])
    return p


def main():
    print("Starting the application...")
    
    # Check Ollama first
    if not check_ollama():
        print("\n⚠️  Continuing anyway, but errors may occur...\n")
    
    try:
        print("\nBuilding graph...")
        graph = build_graph()
        print("Compiling graph...")
        app = graph.compile()
        print("Graph compiled successfully!")

        state = AppState(
            profile=example_profile(),
            job_description="We are hiring a Full Stack Engineer to work on ML infra and front-end with TypeScript and React. Strong experience in LLMs and production systems is a plus.",
            company="BMW",
        )
        print(f"Initial state created with company: {state.company}")

        print("\n" + "="*50)
        print("Executing graph...")
        print("="*50 + "\n")
        
        result = app.invoke(state)

        print("\n" + "="*50)
        print("--- GENERATED LETTER ---")
        print("="*50)
        if result.get("letter"):
            print(result["letter"])
        else:
            print("WARNING: No letter was generated!")
            print(f"Result keys: {list(result.keys())}")
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()