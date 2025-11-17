import os
from dotenv import load_dotenv
from graph import build_graph
from state import AppState, ExperienceItem, Profile
import json
from util.json_parser import load_job_json
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

        # Load resume.json and parse into Profile object
        resume_path = os.path.join(os.path.dirname(__file__), "input", "resume.json")
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)
        
        profile = Profile(**resume_data)
        
        # Load job.json and extract job description and company
        # The load_job_json function handles unescaped newlines automatically
        job_path = os.path.join(os.path.dirname(__file__), "input", "job.json")
        job_data = load_job_json(job_path)
        
        job_description = job_data.get("job_description", "")
        company = job_data.get("company", None)
        
        if not job_description:
            raise ValueError("job_description is required in job.json")
        
        state = AppState(
            profile=profile,
            job_description=job_description,
            company=company,
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