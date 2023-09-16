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
QDRANT_LOCATION = "https://hackzurich23-vectordb-emcg5a6iia-oa.a.run.app/"
QDRANT_PORT = 443
PATH_TO_PDFS = "./docs/"
PDF_MASK = "*.pdf"
CHUNK_SIZE = 600


def list_pdf_files(list_pattern):
    return glob.glob(list_pattern)


def convert_files_to_text(paths):
    texts = []
    for i, path in enumerate(paths):
        text = ""
        with open(path, "rb") as file:
            print(f"Reading file {path}...", "\n")
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if "table of contents" in page_text:
                    continue
                text += page_text
        texts.append(text.replace("\t", " "))
    return texts


def convert_file_to_text(path):
    print(f"Reading file {path}...", "\n")
    text = ""
    with open(path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if "table of contents" in page_text:
                continue
            text += page_text
    text = text.replace("\t", " ")
    return text


def chunk_text(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=CHUNK_SIZE, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)


def chunk_texts(texts):
    chunks = []
    for text in texts:
        chunks.extend(chunk_text(text))
    return chunks


def generate_vectors(text_chunks, embeddings: OpenAIEmbeddings):
    points = []
    for chunk in text_chunks:
        print(f"Generating vector for the chunk of length {len(chunk)}", "\n")
        embed_result = embeddings.embed_query(chunk.replace("\n", " "))
        points.append(PointStruct(id=str(uuid.uuid4()), vector=embed_result, payload={"text": chunk}))
    return points


def upsert_vectors(vectors, client: QdrantClient):
    print(f"Upserting {len(vectors)} vectors...", "\n")
    client.upsert(collection_name=QDRANT_COLLECTION_NAME, wait=True, points=vectors)


def initialise_qdrant_collection(name, location, port):
    client = QdrantClient(location=location, port=port)
    try:
        client.get_collection(collection_name=name)
    except:
        print(f"Collection {name} doesn't exist. Creating...", "\n")
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


def process_file(path, embeddings: OpenAIEmbeddings, client: QdrantClient):
    print(f"Textifying the file {path}...", "\n")
    text = convert_file_to_text(path)
    print("Chunking text data...", "\n")
    chunks = chunk_text(text)
    print(f"Generating vectors for file {path}...", "\n")
    vectors = generate_vectors(chunks, embeddings)
    print(f"Upserting the vectors to Qdrant for file {path}...", "\n")
    upsert_vectors(vectors, client)
    print(f"File {path} done.", "\n")


def main():
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_PRIVATE_KEY")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    client = initialise_qdrant_collection(QDRANT_COLLECTION_NAME, QDRANT_LOCATION, QDRANT_PORT)

    print(f"Enumerating PDF files in {PATH_TO_PDFS}...", "\n")
    paths = list_pdf_files(PATH_TO_PDFS + PDF_MASK)
    print(f"PDF files found: {len(paths)}. Processing...", "\n")
    for path in paths:
        process_file(path, embeddings, client)

    print("All files done. Vectors uploaded.")


if __name__ == '__main__':
    main()
