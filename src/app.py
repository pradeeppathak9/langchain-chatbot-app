import os
import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from langchain.llms import Cohere
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

llm_to_use = 'openai'

@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    memory = ConversationBufferMemory()
    if llm_to_use == 'cohere':
        llm = Cohere(
            cohere_api_key=os.environ['COHERE_API_KEY'], 
            temperature=0.0
        )
    elif llm_to_use == 'openai':
        llm = ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            temperature=0.0
        )
    else:
        model_id = "tiiuae/falcon-7b-instruct"
        llm = HuggingFaceHub(
            huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_KEY"],
            repo_id=model_id,
            model_kwargs={"temperature":0.7, "max_new_tokens":500}
        )

    
    llm_chain = ConversationChain(
            llm=llm,
            memory = memory,
            verbose=True
    )

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)



@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = llm_chain.predict(input=message)

    # Do any post processing here

    # Send the response
    await cl.Message(content=res).send()
    

# chainlit run app.py -w
