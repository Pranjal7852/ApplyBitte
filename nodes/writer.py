from langchain_ollama import OllamaLLM
import os

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
llm = OllamaLLM(model=OLLAMA_MODEL)

LETTER_PROMPT = """
You are an expert cover letter writer. Given the candidate profile JSON, company research summary, job requirements JSON, and matching points array, write a professional 3-4 paragraph cover letter tailored to the role. Use specifics from the matching_points and the company research summary. Maintain a professional but warm tone. Output only the final cover letter text.

Profile:
{profile}

Company Research Summary:
{company_research}

Job Requirements:
{jd}

Matching Points:
{matches}

Cover letter:
"""


def writer_node(state):
    print("  → Running writer_node...")
    profile = state.profile
    company_research = state.company_research or ""
    jd = state.jd_requirements or {}
    matches = state.matching_points or []

    try:
        print("  → Calling LLM to generate cover letter...")
        # Support both Pydantic v1 and v2
        if hasattr(profile, 'model_dump_json'):
            profile_json = profile.model_dump_json()
        elif hasattr(profile, 'json'):
            profile_json = profile.json()
        else:
            import json
            profile_json = json.dumps(profile.model_dump() if hasattr(profile, 'model_dump') else profile.dict())
        prompt = LETTER_PROMPT.format(
            profile=profile_json,
            company_research=company_research or "",
            jd=jd,
            matches='\\n'.join(matches) if isinstance(matches, list) else str(matches),
        )
        out = llm.invoke(prompt)
        print("  → Cover letter generated successfully!")
        return {"letter": out}
    except Exception as e:
        print(f"  ❌ Error in writer_node: {e}")
        import traceback
        traceback.print_exc()
        return {"letter": None}