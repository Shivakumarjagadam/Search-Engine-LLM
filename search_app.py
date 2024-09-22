import streamlit as st 
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun # duck--it used to serch results from internet..
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler # imp to manily interface..
#code...
import os
from dotenv import load_dotenv
load_dotenv()

#Arxiv and wikipedia tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

search=DuckDuckGoSearchRun(name="Search")

st.title("Langchain -chat with search")
""" In this example we are using streamlit callbackhandler to display the thoughts and actions of an agent in an interactive streamlit app..

try langchain stramlit agent eg: at [github.com/langchain-ai/streamlit-agent]


"""

#sidebar for settings...
st.sidebar.title("Settings")
groq_api_key=st.sidebar.text_input("enter your GROQ api key:",type="password")

if "messages" not in st.session_state:
  st.session_state["messages"]=[
    {"role":"assisstant","content":"hi,im a chatbot who can search the web,how can i help you?"}
  ]
  
for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg['content'])
  
if prompt:=st.chat_input(placeholder="what is machine learning?"):
  st.session_state.messages.append({"role":"user","content":prompt})
  st.chat_message("user").write(prompt)
  


  
  llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192",streaming=True)
  tools=[search,arxiv,wiki]
  search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
  
  
  with st.chat_message("assistant"):
    
    st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
    response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
    st.session_state.messages.append({"role":"assistant","content":response})
    st.write(response)
    
    
