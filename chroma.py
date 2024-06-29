import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI


# Load the enivronment variables and API keys 
load_dotenv(".env") 
key = os.environ["OPENAI_KEY"]

# Call the model and parser for extracting the output of LLM
parser = StrOutputParser()
llm = ChatOpenAI(model="gpt-3.5-turbo",api_key=key)


# Store the vectrostores locally
def chroma_save(path,key=key):
    #Load the docs
    loader = PyPDFLoader(path)
    doc = loader.load()

    # Split the doc content
    tex_splitter = RecursiveCharacterTextSplitter(chunk_size = 9000, chunk_overlap = 1000)
    splits = tex_splitter.split_documents(doc)

    # Store the content
    vs = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=key), persist_directory="chroma-laws")
    vs.add_documents(documents=splits)
    vs.as_retriever()
    print("saved: " + str(path))


def main():
    data = os.path.join('resources', 'pdfs')
    docs = os.listdir(data)

    # save every file to the loacal database
    for doc in docs:
        doc_path = os.path.join(data,doc)
        chroma_save(doc_path)



if __name__ == "__main__":
    main()
