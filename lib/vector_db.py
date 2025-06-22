from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from typing import List
from langchain_core.documents import Document
from lib.config import settings


def create_vector_db():
    es_url = settings.es_url
    index_name = "document_index"
    # hf_api_key = settings.huggingface_api_key
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
    )

    return ElasticsearchStore(
        es_url=es_url,
        index_name=index_name,
        embedding=embeddings,
        strategy=ElasticsearchStore.ApproxRetrievalStrategy(),
    )


vector_store = create_vector_db()


def add_documents(documents: List[Document], user_id: str):
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata["user_id"] = user_id

    vector_store.add_documents(documents)


def search_documents(query: str, user_id: str, top_k: int = 3) -> str:
    if user_id is None or user_id == "":
        raise ValueError("User ID cannot be None or empty")
    es_filter = [{"term": {"metadata.user_id": user_id}}]

    results = vector_store.similarity_search(
        query,
        k=top_k,
        filter=es_filter,
    )
    context = "\n\n".join([doc.page_content for doc in results])
    return context
