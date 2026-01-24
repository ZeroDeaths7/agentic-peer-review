import operator
from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import BaseMessage

# This function allows LangGraph to append new messages to the history 
# rather than overwriting the whole list every time.
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Represents the state of the Socratic Peer Review graph.
    
    Attributes:
        messages: The conversation history. 'add_messages' ensures new messages 
                  are appended to this list.
        next_speaker: The name of the agent (node) that the Supervisor has 
                      decided should speak next.
        debate_round: A counter to track how many back-and-forth turns have 
                      occurred. Used to enforce a limit (e.g., max 5 turns).
    """
    
    # The primary conversation history. 
    # Storing as BaseMessage allows us to handle HumanMessage, AIMessage, 
    # and ToolMessage (from the Librarian) natively.
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Metadata for the Supervisor logic
    next_speaker: str
    debate_round: int