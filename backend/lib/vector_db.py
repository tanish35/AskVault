from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain_core.documents import Document
from lib.config import settings
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams


def create_vector_db():
    collection_name = "document_index"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )

    existing_collections = [
        col.name for col in qdrant_client.get_collections().collections
    ]
    if collection_name not in existing_collections:
        print(f"Collection '{collection_name}' not found. Creating it now.")
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print("Collection created.")

    collection_info = qdrant_client.get_collection(collection_name=collection_name)

    user_id_index_key = "metadata.user_id"

    if user_id_index_key not in collection_info.payload_schema:
        print(f"Payload index for '{user_id_index_key}' not found. Creating it now.")
        qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name=user_id_index_key,
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        print("Payload index created.")

    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embeddings,
    )


vector_store = create_vector_db()


def add_documents(documents: List[Document], user_id: str):
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata["user_id"] = user_id

    vector_store.add_documents(documents)


def search_documents(query: str, user_id: str, top_k: int = 5) -> str:
    if not user_id:
        raise ValueError("User ID cannot be None or empty")

    filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.user_id",
                match=models.MatchValue(value=user_id),
            )
        ]
    )

    results = vector_store.similarity_search(
        query=query,
        k=top_k,
        filter=filter,
    )

    context = "\n\n".join([doc.page_content for doc in results])
    return context
