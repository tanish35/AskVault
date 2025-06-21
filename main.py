import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from lib.config import settings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from unstructured.partition.auto import partition

from lib.vector_db import add_documents
from lib.agents import create_qa_crew


app = FastAPI(title="Document Q&A API")


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
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

        add_documents(documents=chunked_docs)

        return {"filename": file.filename, "status": "processed and indexed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


class Question(BaseModel):
    query: str


@app.post("/chat")
async def chat_with_agent(question: Question):
    qa_crew = create_qa_crew(question.query)
    result = qa_crew.kickoff()
    print(f"QA Crew Result: {result}")
    return {"answer": result}
