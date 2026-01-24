from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import (
    supervisor_node,
    proponent_node,
    critic_node,
    librarian_node,
    novelty_node,
    methodology_node
)

workflow = StateGraph(GraphState)

# 2. Add All Nodes (The Agents)
# The string names here MUST match the strings returned by the Supervisor
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Proponent", proponent_node)
workflow.add_node("Critic", critic_node)
workflow.add_node("Librarian", librarian_node)
workflow.add_node("Novelty_Detector", novelty_node)
workflow.add_node("Methodology_Auditor", methodology_node)

workflow.set_entry_point("Supervisor")


def get_next_node(state: GraphState):
    return state["next_speaker"]

workflow.add_conditional_edges(
    "Supervisor",        # The node where the decision is made
    get_next_node,       # The function that determines the next path
    {
        # Map the string returned by Supervisor to the actual Node Name
        "Proponent": "Proponent",
        "Critic": "Critic",
        "Librarian": "Librarian",
        "Novelty_Detector": "Novelty_Detector",
        "Methodology_Auditor": "Methodology_Auditor",
        "End": END  # Special LangGraph node to finish execution
    }
)



workflow.add_edge("Proponent", "Supervisor")
workflow.add_edge("Critic", "Supervisor")
workflow.add_edge("Librarian", "Supervisor")
workflow.add_edge("Novelty_Detector", "Supervisor")
workflow.add_edge("Methodology_Auditor", "Supervisor")


app = workflow.compile()