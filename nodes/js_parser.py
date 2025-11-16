from langchain_ollama import OllamaLLM
import os

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
llm = OllamaLLM(model=OLLAMA_MODEL)

JD_PROMPT = """
Parse the job description and return JSON with the fields:
- title
- responsibilities (array)
- required_skills (array)
- preferred_skills (array)
- experience_level

Job Description:
{jd}

Respond only with valid JSON.
"""


def jd_parser_node(state):
    print("  → Running jd_parser_node...")
    jd = state.job_description or ""
    if not jd:
        print("  ⚠️  No job description provided, skipping parsing")
        return {}
    
    try:
        print("  → Calling LLM to parse job description...")
        out = llm.invoke(JD_PROMPT.format(jd=jd))
        print("  → LLM response received")
        import json
        try:
            parsed = json.loads(out)
            print("  → Successfully parsed JSON response")
        except Exception:
            print("  → Failed to parse JSON, asking LLM to reformat...")
            # ask to reformat strictly
            followup = llm.invoke("Reformat the following strictly as JSON:\n" + out)
            try:
                parsed = json.loads(followup)
                print("  → Successfully parsed reformatted JSON")
            except Exception:
                print("  ⚠️  Could not parse JSON, using fallback structure")
                parsed = {"title": None, "responsibilities": [], "required_skills": [], "preferred_skills": [], "experience_level": None}
        return {"jd_requirements": parsed}
    except Exception as e:
        print(f"  ❌ Error in jd_parser_node: {e}")
        import traceback
        traceback.print_exc()
        return {"jd_requirements": {}}