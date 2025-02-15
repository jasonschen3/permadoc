from llama_index.core import SimpleDirectoryReader
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
import dill as pickle


def getresponse(input):
        # Load the index
    with open('index.pkl', 'rb') as f:
        index = pickle.load(f)
        # setting up the llm
    llm = Ollama(model="llama3", request_timeout=120.0)

        # ====== Setup a query engine on the index previously created ======
    Settings.llm = llm # specifying the llm to be used
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=4)

        # === Prompt Template
    # query_str = input("Enter your queary: ") #Taken from user input
    query_str = input

    context_results = query_engine.retrieve(query_str)
    context_str = "\n".join([result.node.text for result in context_results])

    template = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information above I want you to think step by step to answer the query in a crisp manner, in case you don't know the answer say 'I don't know!'. \n"
        "Query: {query_str}\n"
        "Answer: "
    )

    qa_template = PromptTemplate(template)
    prompt = qa_template.format(context_str=context_str,query_str=query_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": prompt})
    response = llm.complete(prompt + "and here is the context: " + context_str)
    print(response)
    return response


