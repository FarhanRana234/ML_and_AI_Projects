import streamlit as st
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# Use Streamlit secrets for OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Define tools
@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user."""
    return f"Hello {name}, I hope you're well today :)"

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations."""
    return f"The sum of {a} and {b} is {a + b}."

# Initialize model and tools
model = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
tools = [say_hello, calculator]

# Streamlit layout
st.title("🤖 AI Assistant using OpenAI API & LangChain")
st.markdown("Ask me to perform calculations, greet you, or just chat casually! You can even give me a **personality twist** 👇")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "personality" not in st.session_state:
    st.session_state.personality = "Be friendly and helpful."

# Sidebar for customization
with st.sidebar:
    st.header("🧠 Assistant Personality")
    st.write("Set how the assistant should behave.")
    custom_prompt = st.text_area(
        "Enter custom behavior or tone (e.g. 'Be humorous and sarcastic', 'Be like Tony Stark')",
        value=st.session_state.personality,
        height=80
    )
    if st.button("Save Personality"):
        st.session_state.personality = custom_prompt
        st.success("Personality updated!")

# Create agent
agent_executor = create_react_agent(model, tools)

# Chat input
user_input = st.text_input("💬 Your message:")

if st.button("Send") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Apply personality as a system-style message
    combined_input = f"{st.session_state.personality}\n\nUser: {user_input}"

    assistant_response = ""
    for chunk in agent_executor.stream({"messages": [HumanMessage(content=combined_input)]}):
        if "agent" in chunk and "messages" in chunk["agent"]:
            for message in chunk["agent"]["messages"]:
                assistant_response += message.content

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# Display chat history
st.markdown("---")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"🧍‍♂️ **You:** {chat['content']}")
    else:
        st.markdown(f"🤖 **Assistant:** {chat['content']}")
