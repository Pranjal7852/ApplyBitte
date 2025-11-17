from langchain_ollama import OllamaLLM
import os

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
llm = OllamaLLM(model=OLLAMA_MODEL)

MATCH_PROMPT = """
Given the candidate profile (JSON) and the parsed job requirements (JSON), produce a JSON array called "matching_points" where each entry is a short sentence describing how the candidate matches a specific requirement. Use specific bullet points from the profile when possible.

Profile:
{profile}

Job Requirements:
{jd}

Respond only with JSON array.
"""


def matcher_node(state):
    print("  → Running matcher_node...")
    profile = state.profile
    jd = state.jd_requirements
    if not (profile and jd):
        print("  ⚠️  Missing profile or jd_requirements, skipping matching")
        return {}
    
    try:
        print("  → Calling LLM to match profile with job requirements...")
        # Support both Pydantic v1 and v2
        if hasattr(profile, 'model_dump_json'):
            profile_json = profile.model_dump_json()
        elif hasattr(profile, 'json'):
            profile_json = profile.json()
        else:
            import json
            profile_json = json.dumps(profile.model_dump() if hasattr(profile, 'model_dump') else profile.dict())
        prompt = MATCH_PROMPT.format(profile=profile_json, jd=jd)
        out = llm.invoke(prompt)
        print("  → LLM response received")
    except Exception as e:
        print(f"  ❌ Error in matcher_node: {e}")
        import traceback
        traceback.print_exc()
        return {"matching_points": []}
    import json
    try:
        parsed = json.loads(out)
        # Handle both cases: LLM might return a list directly or a dict with "matching_points" key
        if isinstance(parsed, dict) and "matching_points" in parsed:
            matches = parsed["matching_points"]
        elif isinstance(parsed, list):
            matches = parsed
        else:
            # Unexpected format, try to extract as list
            matches = list(parsed.values())[0] if isinstance(parsed, dict) and parsed else []
    except Exception:
        # fallback: parse lines
        lines = [l.strip('- ').strip() for l in out.splitlines() if l.strip()]
        matches = lines
    
    # Ensure matches is always a list
    if not isinstance(matches, list):
        matches = []
    
    return {"matching_points": matches}