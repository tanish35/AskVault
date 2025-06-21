from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from lib.vector_db import search_documents


@tool("Document Search Tool")
def search_tool(query: str) -> str:
    """Searches the vector database for similar documents based on the query.

    Args:
        query: The search query to find relevant documents

    Returns:
        str: The search results from the vector database
    """
    return search_documents(query)


doc_expert_agent = Agent(
    role="Document Analysis Expert",
    goal="Provide answers to questions by searching through the uploaded documents.",
    backstory=(
        "You are an AI assistant who is an expert in analyzing document contents. "
        "You have a special tool to search the uploaded documents. "
        "Your responses must be based *only* on the information retrieved from the documents."
    ),
    llm="gemini/gemini-2.5-flash",
    tools=[search_tool],  # type: ignore
    verbose=True,
)


def create_qa_crew(query) -> Crew:
    qa_task = Task(
        description=f"Answer the user's question: '{query}'. Use your search tool to find relevant information.",
        expected_output="A helpful and accurate answer based on the retrieved document context.",
        agent=doc_expert_agent,
    )

    return Crew(agents=[doc_expert_agent], tasks=[qa_task], process=Process.sequential)
