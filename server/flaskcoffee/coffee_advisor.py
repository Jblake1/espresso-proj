#coffee_advisor.py

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, chain
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain.prompts import PromptTemplate

# Windows credential manager key retrieval 
# api_key_1 = keyring.get_password("OPENAI_API_KEY", "openai_user")
# os.environ["OPENAI_API_KEY"] = api_key_1


api_key_1 = os.environ.get("OPENAI_API_KEY")

# langchain api was incase I wanted to use langsmith. But seems unnecessary for the scope of this project
# api_key_2 = keyring.get_password("LANGCHAIN_API_KEY", "langchain_user")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
# os.environ["LANGCHAIN_API_KEY"] = api_key_2

llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = InMemoryVectorStore(embeddings)

file = os.path.join(os.path.dirname(__file__), "csv_data", "Espresso_seed_data.csv")
loader = CSVLoader(file_path=file,
    csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Drink', 'Grinder','Espresso Grind Segment', 'Espresso Grind Range', 'Total Machine Grind Range']
})

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index chunks
_ = vector_store.add_documents(documents=all_splits)

# Retriever didn't work with multiple passthroughs. Workaround was to use lambda x in chain
# retriever = vector_store.as_retriever()


def get_coffee_advice(drink, coffee_beans, brewing_device, grinder):
    coffee_setup = {
        "drink": drink,
        "coffee_beans": coffee_beans,
        "brewing_device": brewing_device,
        "grinder": grinder,
    }
    print("Coffee Setup:", coffee_setup)
    

    bean_analysis_prompt = PromptTemplate.from_template(
    """You are an expert barista answering questions for a customer making {drink} at home using the {grinder} grinder and {brewing_device} {drink} machine. 
    The customer has purchased {coffee_beans} beans, but would like to understand the beans' characteristics. Provide a comprehensive description of 
    {coffee_beans} beans including its roast type (light, medium, dark) and density. The following is an example response to a customer who purchased Red Bird 
    Blue Jaguar Espresso beans: \n 
    Red Bird Blue Jaguar Espresso beans are a medium roast bean, designed to balance sweetness, acidity, and body. Being a medium roast, the beans 
    retain moderate density, which means they are neither as dense as light roasts nor as porous as dark roasts.   
    """) 

    bean_segmentation_prompt = PromptTemplate.from_template(
        """"Based on the bean analysis below assign the coffee beans to one of three grind size segments: 1) Fine - Light roasts, single-origin coffees, 
        or beans with high density, 2) Medium - Medium roasts, balanced blends, or beans with medium density, 3) Coarse - Dark roasts or beans with 
        lower density. Respond with only one of three grind sizes: Fine, Medium, Coarse.\n\n

        Bean analysis: {bean_analysis}
    """)

    grind_recommendation_prompt = PromptTemplate.from_template(
        """Answer the question based only on the following context and grind segmentation: \n
    Context: {context}\n
    Bean Segmentation: {bean_segmentation}\n

    Question: What grind range would you recommend to brew {drink} using the {grinder} grinder and {brewing_device}?

    Example response (Do not restate inputs): 12 to 18
    """)

    #Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    bean_analysis_chain = bean_analysis_prompt | llm | StrOutputParser()
    bean_segmentation_chain = bean_segmentation_prompt | llm | StrOutputParser()
    grind_recommendation_chain = grind_recommendation_prompt | llm | StrOutputParser()

    chain = (
        {"bean_analysis" : bean_analysis_chain, "grinder": RunnablePassthrough(), "drink": RunnablePassthrough(), "brewing_device": RunnablePassthrough()} 
        | RunnablePassthrough.assign(bean_segmentation=bean_segmentation_chain)
        | RunnablePassthrough.assign(context=lambda x: format_docs(vector_store.similarity_search("What grind setting would you recommend to brew {drink} using the {grinder} grinder?")))
        | RunnablePassthrough.assign(grind_recommendation=grind_recommendation_chain)
    )


    try:
        result = chain.invoke(coffee_setup)
        print("Result:", result)
        return result
    except Exception as e:
        print("Error in get_coffee_advice:", str(e))
        raise





