import chainlit as cl
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
load_dotenv()

from graph.workflow import app


AVATARS = {
    "Proponent": "👷",
    "Critic": "👩‍⚖️",
    "Librarian": "📚",
    "Novelty_Detector": "🕵️",
    "Methodology_Auditor": "⚙️",
    "Supervisor": "🧠"
}

@cl.on_chat_start
async def start():
    """
    Init the session
    """

    cl.user_session.set("graph", app)

    await cl.Message(
        content = "**Socratic Peer Review Ring Initialized.**\n\nI am ready to critique your research ideas. Please propose a topic or hypothesis.",
        author = "System"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    """
    Main loop: Runs the graph and streams output to the UI.
    """

    graph = cl.user_session.get("graph")
    inputs = {"messages": [HumanMessage(content=message.content)]}
    
    last_message_id = None

    async for event in graph.astream(inputs):
        
        # event of form {'Proponent': {'messages': [AIMessage]}}
        for node_name, value in event.items():
            
            if "messages" in value and value["messages"]:
                new_message = value["messages"][-1]
                content = new_message.content
                
                if hasattr(new_message, "tool_calls") and new_message.tool_calls:
                    async with cl.Step(name=f"{node_name} (Tools)", type="tool") as step:
                        step.input = "Accessing External Knowledge..."
                        step.output = f"Executing: {[t['name'] for t in new_message.tool_calls]}"

                # 2. Final agent responses
                if content:
                    avatar_icon = AVATARS.get(node_name, "🤖")
                    
                    await cl.Message(
                        content=content,
                        author=node_name,
                    ).send()

            # 3. Supervisor decisions displayed (might ignore if too cluttered)
            elif "next_speaker" in value:
    
                next_speaker = value["next_speaker"]
                if next_speaker != "End":
                    await cl.Message(
                        content=f"Routing debate to: **{next_speaker}**",
                        author="Supervisor",
                        parent_id=message.id 
                    ).send()
