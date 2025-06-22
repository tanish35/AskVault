# import os
# from crewai import LLM
# from lib.config import settings


# def init_llm():
#     api_key = settings.google_api_key
#     print(api_key)
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY environment variable is not set.")

#     # Set the API key as environment variable (LiteLLM expects this)
#     os.environ["GOOGLE_API_KEY"] = api_key

#     # Initialize CrewAI's LLM wrapper with LiteLLM
#     llm = LLM(
#         model="gemini/gemini-2.5-flash",
#         temperature=0.7,
#     )

#     return llm


# llm = init_llm()
