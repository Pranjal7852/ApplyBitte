from langgraph.graph import StateGraph, END
from state import AppState
from nodes.company_research import company_research_node
from nodes.js_parser import jd_parser_node
from nodes.macher import matcher_node
from nodes.writer import writer_node


def build_graph():
    graph = StateGraph(AppState)

    graph.add_node("company_research", company_research_node)
    graph.add_node("jd_parser", jd_parser_node)
    graph.add_node("matcher", matcher_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("company_research")

    graph.add_edge("company_research", "jd_parser")
    graph.add_edge("jd_parser", "matcher")
    graph.add_edge("matcher", "writer")
    graph.add_edge("writer", END)

    # Conditional fallback examples (pseudocode):
    # graph.add_conditional_edge("company_research", lambda s: "jd_parser" if s.company_research else "backup_research")

    return graph