# Bavarian law RAG app

 

## Ⅰ Introduction

This app aims to ease the process of obtaining legal information, simplifying it for better comprehension and making potential connections between different laws.
It leverages data scraped from www.gesetze-bayern.de website and gpt-3.5-turbo for Retrieval Augmented Generation.

* Link to database on Huggingface: https://huggingface.co/datasets/gunslinger7/bavarian_law_database


## Ⅱ Implementing

![rag](https://github.com/gunslinger7/rag_lawyer/assets/167663925/2e419e74-7516-484b-aa7f-6e1dfff6cabe)

My initial plan was to use an Open Source LLM with its Embeddings, that could generate quality text in German and could run locally or on Colab. But after testing many models under 10 billion parameters like falcon-7b, phi-1.5b and etc. it was clear that I needed a more powerful model.
I chose GPT-3.5-Turbo beacuse it was cheaper than the newer models and OpenAI Embeddings which are way faster than the ones that run locally.
As for local vector database, my choice landed on ChromaDB as it was free and fairly simple to implement it in Langchain. 
And to make things look nicer I used Streamlit for User Interface.

## Ⅲ Scraping the Data
The task consisted of 2 steps:
1. Getting the list of all the law abbreviations (e.g. BayRS, BayAlmG)
2. Putting every abbreviation into standard pdf download file link of this from "https://www.gesetze-bayern.de/Content/Pdf/ABBREVIATION?all=True".

Ironically this was the most pain-in-the-ass part of the whole project, although it should have been the quickest and simplest.

Why? Usually getting links via requests module in python is extremely simple, but not in the case of JavaScript rendered web pages, that return incomplete html files (with more than half of the html file missing which is easily obtainable via web-browsers inspector). It also happens to be that selenium module doesn't return full html neither. 

Hence the only choice was to save all source htmls manually by going through 24 pages in browser. Thankfully, it took me around 90 seconds to do it.

 ## Ⅳ Putting all together
It was time to assemble the app, so I:

• Donwloaded, chunked and saved the pdfs on a local database
```
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
```

• Created a LLM RAG chain with conversation history 
```
    # Compile the final chain and return it
    qa_chain = create_stuff_documents_chain(llm, instruct_prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)
    
```

• Created a simple Streamlit GUI for it

![Screenshot (53)](https://github.com/gunslinger7/rag_lawyer/assets/167663925/48c36a0c-d102-485e-9ad0-c4f5f167c78d)

### 'Les Gutmann' is 'Alles gut Man' as 'Saul Goodman' is 'It's all good man'

## Ⅴ Testing

The app uses RAG which means first it searches for the most similar context to provide for the LLM as context, which is why users should try to be more specific and use keywords if possible.

Here are some of the examples of the app in action:

![Screenshot (57)](https://github.com/gunslinger7/rag_lawyer/assets/167663925/87dca6f1-cb29-42f6-bef3-d2886799ed13)


![Screenshot (58)](https://github.com/gunslinger7/rag_lawyer/assets/167663925/908487c2-6463-4e53-bf69-d3383a650320)


![Screenshot (60)](https://github.com/gunslinger7/rag_lawyer/assets/167663925/85b25bc9-36c1-4681-ae40-c70085bdb556)



## Ⅵ Conclusion

To sum things up, this RAG app successfully manages to find, quote and translate relevant laws, as well as simplify and summarize them in a digestable way also letting the user ask further questions about it. The current objective is to replicate this app using knowledge graphs and compare the results.
