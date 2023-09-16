import uuid
import glob
import os

from langchain.schema import HumanMessage
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

QDRANT_COLLECTION_NAME = "zurizap"
QDRANT_LOCATION = "localhost"
QDRANT_PORT = 6333
PATH_TO_PDFS = "/docs"
PDF_MASK = "*.pdf"


def list_pdf_files(list_pattern):
    return glob.glob(list_pattern)


def convert_to_text(paths):
    texts = []
    for i, path in enumerate(paths):
        text = ""
        with open(path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if "table of contents" in page_text:
                    continue
                text += page_text
        texts.append(text)
    return texts


def chunk_text(text):
    chunk_size = 600  # temporary, to avoid 429 when querying OpenAI
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)


def chunk_texts(texts):
    chunks = []
    for text in texts:
        chunks.extend(chunk_text(text))
    return chunks


def generate_vectors(text_chunks, embeddings: OpenAIEmbeddings):
    points = []
    for chunk in text_chunks:
        embed_result = embeddings.embed_query(chunk)
        points.append(PointStruct(id=str(uuid.uuid4()), vector=embed_result, payload={"text": chunk}))
    return points


def upsert_vectors(vectors, client: QdrantClient):
    client.upsert(collection_name=QDRANT_COLLECTION_NAME, wait=True, points=vectors)


def initialise_qdrant_collection(name, location, port):
    client = QdrantClient('http://localhost:6333')
    #client = QdrantClient(location=location, port=port)
    client.recreate_collection(collection_name=name,
                               vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
    return client


def answer_with_context(query, embeddings: OpenAIEmbeddings, chat: ChatOpenAI, client: QdrantClient, collection_name):
    embedded_query = embeddings.embed_query(query)

    print("You would like to know: ", query, '\n')
    print("Let me think a bit...\n")

    search_result = client.search(collection_name=collection_name, query_vector=embedded_query, limit=3)

    prompt = ""
    for result in search_result:
        prompt += result.payload['text']

    concatenated_answer = " ".join([prompt, query])

    answer = chat(messages=[HumanMessage(content=concatenated_answer)])
    return answer.content


def main():
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_KEY")

    text_data = convert_to_text(list_pdf_files(PATH_TO_PDFS + PDF_MASK))
    chunks = chunk_texts(text_data)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    chat = ChatOpenAI(temperature=0.4, openai_api_key=openai_api_key)

    vectors = generate_vectors(chunks, embeddings)

    client = initialise_qdrant_collection(QDRANT_COLLECTION_NAME, QDRANT_LOCATION, QDRANT_PORT)
    upsert_vectors(vectors, client)

    question = "How am I insured?"
    answer = answer_with_context(question, embeddings, chat, client, QDRANT_COLLECTION_NAME)
    print("The answer is: ", answer, "\n")


if __name__ == '__main__':
    main()


