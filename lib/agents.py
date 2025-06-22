from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from lib.vector_db import search_documents


@tool("Document Search Tool")
def search_tool(query: str, user_id: str) -> str:
    """
    Searches the vector database for documents similar to the given query,
    scoped to a specific user.

    Args:
        query (str): The search query string.
        user_id (str, optional): The user identifier.

    Returns:
        str: Concatenated contents of the top matching documents.
    """
    if not query:
        return "Missing query in search input."
    if not user_id:
        return "Missing user_id in search input."

    try:
        return search_documents(query, user_id)
    except Exception as e:
        return f"Error searching documents: {str(e)}"


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


def create_qa_crew(user_question: str, user_id: str) -> Crew:
    qa_task = Task(
        description=f"""Answer the user's question: '{user_question}'. 
        
        IMPORTANT: When using the Document Search Tool, you MUST use these exact parameters:
        - query: the search query derived from the user's question
        - user_id: {user_id}
        
        Use your search tool to find relevant information from the documents.""",
        expected_output="A helpful and accurate answer based on the retrieved document context.",
        agent=doc_expert_agent,
    )

    return Crew(agents=[doc_expert_agent], tasks=[qa_task], process=Process.sequential)
