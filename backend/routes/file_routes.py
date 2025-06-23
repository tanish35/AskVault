from fastapi import UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from fastapi import APIRouter
import os
from middleware.auth import check_auth


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from unstructured.partition.auto import partition

from lib.vector_db import add_documents
from lib.agents import create_qa_crew

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user=Depends(check_auth)):
    temp_file_path = f"./temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        elements = partition(filename=temp_file_path)
        texts = []
        for el in elements:
            if el.text.strip():
                texts.append(el.text)
        content = "\n\n".join(texts)

        raw_doc = Document(page_content=content, metadata={"source": file.filename})

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunked_docs = text_splitter.split_documents([raw_doc])

        add_documents(documents=chunked_docs, user_id=user.id)

        return {"filename": file.filename, "status": "processed and indexed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


class Question(BaseModel):
    query: str


@router.post("/chat")
async def chat_with_agent(question: Question, user=Depends(check_auth)):
    try:
        qa_crew, memory = create_qa_crew(question.query, user.id)
        result = qa_crew.kickoff()
        print(f"QA Crew Result: {result}")
        memory.save_context({"input": question.query}, {"output": str(result)})
        markdown_response = result.__str__().strip()
        return {"answer": markdown_response}
    except Exception as e:
        print(f"Error in chat_with_agent: {e}")
        return {"error": "An error occurred while processing your question"}
