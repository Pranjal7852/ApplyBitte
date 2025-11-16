from langchain_community.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain_ollama import OllamaLLM

import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss")

llm = OllamaLLM(model=OLLAMA_MODEL)

# Simple search tool using ddg
def ddg_search(query: str, max_results: int = 5):
    try:
        print(f"Searching for {query} with max results {max_results}")
        search = DuckDuckGoSearchRun(max_results=max_results)
        results = search.invoke(query)
        print(f"Results: {results}")
        return results
    except Exception as e:
        print(f"Error in ddg_search: {e}")
        return []


# Utility to join ddg results into a short context
def summarize_search_results(results):
    # DuckDuckGoSearchRun returns a string, so we'll use it directly
    if isinstance(results, str):
        return results
    # If it's a list, process it
    snippets = []
    for r in results[:5]:
        if isinstance(r, dict):
            title = r.get("title", "")
            body = r.get("body", "")
            snippets.append(f"{title}: {body}")
        else:
            snippets.append(str(r))
    return "\n".join(snippets)