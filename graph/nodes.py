import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from pydantic import BaseModel, Field
from typing import Literal, List

# Local Imports
from graph.state import GraphState
from tools import search_tools
from graph.prompts import (
    SUPERVISOR_SYSTEM_PROMPT,
    PROPONENT_SYSTEM_PROMPT,
    CRITIC_SYSTEM_PROMPT,
    LIBRARIAN_SYSTEM_PROMPT,
    NOVELTY_SYSTEM_PROMPT,
    METHODOLOGY_SYSTEM_PROMPT
)


llm_flash = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5
)

llm_pro = ChatGroq(
    model="openai/gpt-oss-120b", 
    temperature=0.7
)


def execute_tools_inline(response, tools_list):
    """
    Helper to execute tool calls immediately within the node.
    This prevents the need for complex conditional edges in the main graph.
    """
    tool_map = {t.name: t for t in tools_list}
    tool_outputs = []
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        if tool_name in tool_map:
            print(f"   [Tool Exec] Running {tool_name} with {tool_args}...")
            # Execute the tool
            result = tool_map[tool_name].invoke(tool_args)
            
            # Create the ToolMessage (standard LangChain format)
            tool_outputs.append(
                ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=str(result),
                    name=tool_name
                )
            )
            
    return tool_outputs


class RouteSchema(BaseModel):
    """
    Schema for routing decisions made by the Supervisor.
    """
    next_speaker: Literal[
        "Proponent", 
        "Critic", 
        "Librarian",
        "Novelty_Detector",
        "Methodology_Auditor", 
        "End"] = Field(description="The next agent node to activate.")
    reasoning: str = Field(description="The reasoning behind the routing decision.")


def supervisor_node(state: GraphState):
    """
    Supervisor node that routes the conversation
    """
    messages = state["messages"]
    current_round = state.get("debate_round", 0)
    
    if current_round >= 10:
        return {"next_speaker": "End"}

    # 2. Prepare Context
    last_msg = messages[-1]
    last_speaker = "User"
    if hasattr(last_msg, "name") and last_msg.name:
        last_speaker = last_msg.name
        
    system_prompt = SUPERVISOR_SYSTEM_PROMPT.format(
        debate_round=current_round,
        last_speaker=last_speaker
    )
    
    structured_llm = llm_flash.with_structured_output(RouteSchema)
    
    try:
        decision = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            *messages
        ])
        next_node = decision.next_speaker
    except Exception as e:
        # Fallback
        print(f"Supervisor Error: {e}")
        next_node = "End"

    print(f"Supervisor Decided: {next_node} (Round {current_round})")
    return {"next_speaker": next_node}





def proponent_node(state: GraphState):

    """
    Proponent node that advocates for the user's idea.
    """
    response = llm_pro.invoke([
        SystemMessage(content=PROPONENT_SYSTEM_PROMPT),
        *state["messages"]
    ])
    response.name = "Proponent"
    
    return {
        "messages": [response], 
        "current_speaker": "Proponent",
        "debate_round": state.get("debate_round", 0) + 1
    }




def critic_node(state: GraphState):
    response = llm_pro.invoke([
        SystemMessage(content=CRITIC_SYSTEM_PROMPT),
        *state["messages"]
    ])
    response.name = "Critic"
    
    return {
        "messages": [response], 
        "current_speaker": "Critic"
    }




def librarian_node(state: GraphState):
    """
    Uses Gemini Flash to call tools and summarize findings.
    """
    messages = state["messages"]
    
    llm_with_tools = llm_flash.bind_tools(search_tools)
    
    response_1 = llm_with_tools.invoke([
        SystemMessage(content=LIBRARIAN_SYSTEM_PROMPT),
        *messages
    ])
    
    if response_1.tool_calls:
        tool_results = execute_tools_inline(response_1, search_tools)
        
        synthesis_messages = [
            SystemMessage(content=LIBRARIAN_SYSTEM_PROMPT),
            *messages,
            response_1, 
            *tool_results,
            SystemMessage(content="You have the search results. Now synthesize the findings into a clear response. Do NOT use tools again.")
        ]
        
        final_response = llm_with_tools.invoke(synthesis_messages)
        final_response.name = "Librarian"
        return {"messages": [final_response], "current_speaker": "Librarian"}
    
    else:
        response_1.name = "Librarian"
        return {"messages": [response_1], "current_speaker": "Librarian"}
    




def novelty_node(state: GraphState):
    """
    Checks for prior art using tools.
    """
    messages = state["messages"]
    llm_with_tools = llm_flash.bind_tools(search_tools)
    
    response_1 = llm_with_tools.invoke([
        SystemMessage(content=NOVELTY_SYSTEM_PROMPT),
        *messages
    ])
    
    if response_1.tool_calls:
        tool_results = execute_tools_inline(response_1, search_tools)
        
        synthesis_messages = [
            SystemMessage(content=NOVELTY_SYSTEM_PROMPT),
            *messages,
            response_1,
            *tool_results,
            SystemMessage(content="You have the search results. Now synthesize the findings into a clear response. Do NOT use tools again.")
        ]
        final_response = llm_with_tools.invoke(synthesis_messages)
        final_response.name = "Novelty_Detector"
        return {"messages": [final_response], "current_speaker": "Novelty_Detector"}
    
    else:
        response_1.name = "Novelty_Detector"
        return {"messages": [response_1], "current_speaker": "Novelty_Detector"}




def methodology_node(state: GraphState):
    response = llm_pro.invoke([
        SystemMessage(content=METHODOLOGY_SYSTEM_PROMPT),
        *state["messages"]
    ])
    response.name = "Methodology_Auditor"
    
    return {
        "messages": [response], 
        "current_speaker": "Methodology_Auditor"
    }