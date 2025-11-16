from util.tools import ddg_search, summarize_search_results
from langchain_ollama import OllamaLLM
import os

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")
llm = OllamaLLM(model=OLLAMA_MODEL)

RESEARCH_PROMPT = """
You are a researcher. Given the following short search snippets about a company, extract:
1) A brief 2-3 sentence company summary
2) Top 3 company values (as a JSON array)
3) Top 3 products (as a JSON array)
Snippets:
{snippets}

Respond as JSON with keys: summary, values, products
"""


def company_research_node(state):
    print("  → Running company_research_node...")
    company = state.company
    if not company:
        print("  ⚠️  No company specified, skipping research")
        return {}

    print(f"  → Researching company: {company}")
    try:
        q = f"{company} company values products latest news"
        results = ddg_search(q, max_results=6)
        snippets = summarize_search_results(results)
        print(f"  → Got {len(snippets)} characters of search results")

        prompt = RESEARCH_PROMPT.format(snippets=snippets)
        print("  → Calling LLM for company research...")
        out = llm.invoke(prompt)
        print("  → LLM response received")
    except Exception as e:
        print(f"  ❌ Error in company_research_node: {e}")
        import traceback
        traceback.print_exc()
        return {}

    # Simple parsing; for production use robust JSON parsing/validation
    import json
    try:
        parsed = json.loads(out)
    except Exception:
        # fallback: ask LLM to reformat strictly as JSON
        followup = llm.invoke("Reformat the following text strictly as JSON:\n" + out)
        try:
            parsed = json.loads(followup)
        except Exception:
            parsed = {"summary": snippets, "values": [], "products": []}

    return {
        "company_research": parsed.get("summary"),
        "company_values": parsed.get("values"),
        "company_products": parsed.get("products"),
    }