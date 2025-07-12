import streamlit as st
import time
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import AstraDBChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import cassio
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
import os
from dotenv import load_dotenv
load_dotenv()


st.title("Dharmbantu")
st.markdown("Your pocket Indian law assistant.")


if "env_vars_set" not in st.session_state:
    os.environ["ASTRA_DB_APPLICATION_TOKEN"]=st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
    os.environ["ASTRA_DB_ID"]=st.secrets["ASTRA_DB_ID"]
    st.session_state.env_vars_set=True


if "cassio_initialized" not in st.session_state:
    with st.spinner("Connecting to serverless DB"):
        cassio.init(
            token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
            database_id=os.environ["ASTRA_DB_ID"]
        )
        st.session_state.cassio_initialized=True


api_key=st.sidebar.text_input("Enter your OpenAI API key:", type="password")
session_id=st.sidebar.text_input("User ID", value="default_session")

if api_key:
    llm=ChatOpenAI(api_key=api_key)
    embeddings=OpenAIEmbeddings(api_key=api_key)
    
    st.session_state.astra_vector_store=Cassandra(
    embedding=embeddings,
    table_name="Dharmbantu",
    session=None,
    keyspace=None
    )

    st.session_state.astra_vector_index=VectorStoreIndexWrapper(vectorstore=st.session_state.astra_vector_store)
    retriever=st.session_state.astra_vector_store.as_retriever(search_type="mmr",search_kwargs={"k": 5,"fetch_k":30,"lambda_mult":0.5})

    system=(
    "You are given a chat history where the user is asking questions about Indian law."
    "Act as an exceptionally skilled and experienced legal analyst."
    "Carefully study the entire conversation to extract important legal context, facts, and user intent."

    "Then, using all the insights from the chat history, rewrite the user's input question so that it is clear, legally relevant, and context-rich, making it easier to retrieve accurate and helpful information."
    )

    prompt_for_history=ChatPromptTemplate.from_messages([
        ('system',system),
        MessagesPlaceholder("chat_history"),
        ("human","{input}")
    ])

    history_ret=create_history_aware_retriever(prompt=prompt_for_history,llm=llm,retriever=retriever)
    main_prompt=(
        "You are a friendly and highly skilled legal assistant specialized in Indian law. "
        "Given the full chat history and the user's latest message, analyze the situation carefully. "
        "The primary aim is to give all the sections, laws and acts under Bharatiya Nyaya Sanhita,Bharatiya Nagarik Suraksha Sanhita,Bharatiya Sakshya Adhiniyam,Code of Civil Procedure that are applicable regarding the input problem by user.Do not use your knowledge only use the context to return these."
        "You must give the sections and acts in the firsct place"
        "Identify any relevant laws, sections, rights, or legal procedures that apply to the user's described issue in the context provided. "
        "If the situation involves a legal offense or violation, explain the relevant laws and guide the user on what actions they can take. "
        "If no unlawful action is detected, kindly inform the user that the issue does not currently qualify as a legal offense. "
        "Always explain things in formal tone to make legal terms easy to understand."
        "Make sure that you provide all the section,laws,acts that are provided in the context regarding BNS,BNSS,BSA,CPC and all the acts"
        "Do not involve your knowledge, use only the context provided, do not cross the lines of the context.Use only this context data because the outside data may corrupt the answer"
        "Make sure acts and sections under the Bharatiya Nyaya Sanhita,Bharatiya Nagarik Suraksha Sanhita,Bharatiya Sakshya Adhiniyam,Code of Civil Procedure are returned as per the respective mentions in the contexts."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", main_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    stuff_chain=create_stuff_documents_chain(llm,qa_prompt)
    ret_chain=create_retrieval_chain(history_ret,stuff_chain)



    def get_history(session_id: str) -> BaseChatMessageHistory:
        return AstraDBChatMessageHistory(
            session_id=session_id,
            token=st.secrets["ASTRA_DB_APPLICATION_TOKEN"],
            astra_db_id=st.secrets["ASTRA_DB_ID"],
            table_name="dharmbantu_messages"
        )

    final_chain=RunnableWithMessageHistory(
        ret_chain,
        get_history,
        input_messages_key="input",
        output_messages_key="answer",
        history_messages_key="chat_history"
    )
    
    
    user_input=st.text_input("What is the case:")
    if user_input:
        session_history=get_history(session_id)
        start=time.process_time()
        response=final_chain.invoke(
            {"input":user_input},
            config={"configurable":{"session_id": session_id}}
        )
        stop=time.process_time()
        st.write(f"⏱️ Time taken:{stop-start:.2f} seconds")
        st.write("Dharmbantu:",response['answer'])
        with st.expander("Chat History"):
            st.write("Chat History:",session_history.messages)
else:
    st.warning("Please enter the OpenAI API Key.")
