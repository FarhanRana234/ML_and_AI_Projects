from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

@tool
def say_hello(name : str) -> str:
    """Useful for greeting a user."""
    print("Tool has been called.")
    return f"Hello {name}, I hope you're well today :)"
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arthimetic calculations with numbers."""
    print("Tool has been called.")
    return f"the sum of {a} and {b} is {a + b}."

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator, say_hello]
    agent_executor = create_react_agent(model, tools)

    print("Welcome Im your Ai assistant, Type 'quit' to exit.")
    print("You can ask me to perfrom calculations, or casually chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages" : [HumanMessage(content= user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end='')
        print()
if __name__ == "__main__":
    main()
        




