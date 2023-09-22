from langchain import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

with open("./TEST_chat/api_key", "r", encoding="utf-8") as key:
    api_key = key.read()

with open("./TEST_chat/HF_api_key", "r", encoding="utf-8") as key:
    HF_api_key = key.read()

embeddings_model_name="all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, model_kwargs={'device' : 'cpu'})
vectorstore2 = Chroma(persist_directory = "./TEST_Chat/chroma", embedding_function=embeddings)


def chat(llm_info = None, kMos = 100, question = ""):
    
    print(len(vectorstore2.get()["documents"]))
    print("LOG : chat trigerred")
    #user_message = input('Quelle questinon souhaitez vous poser ? :\n')
    llmOAI = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo-16k")

    prompt_template = """
    1. Utilise uniquement les informations données en contexte pour répondre de manières longues et détaillées aux questions posées.
    2. Si l'information n'est pas présente dans les documents en contexte, n'invente pas de réponse.
    3. Répond points par points.
    {context}
    Question: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context","question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}

    match llm_info:
        case "MOSAIC":
            
            repo_id = "mosaicml/mpt-30b-chat"

            llmMos = HuggingFaceHub(
                huggingfacehub_api_token = HF_api_key,
                repo_id = repo_id
            )

            user_message = "qu'est-ce que l'Institut des Sciences de l'Homme (ISH) ?"
            # "Quels sont les principaux choix stratégiques apportés par Millénaire 3 ?"

            score_threshold = 0.2
                
            qa = RetrievalQA.from_chain_type(llm=llmMos, 
                                        chain_type="stuff", 
                                        retriever=vectorstore2.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": kMos, "score_threshold" : score_threshold}), 
                                        return_source_documents=True, 
                                        chain_type_kwargs=chain_type_kwargs
                                        )
            out = qa({"query" : question})

        case "OAI":
            
                score_threshold = 0.1

                while True:
                        
                    qa = RetrievalQA.from_chain_type(llm=llmOAI, 
                                                chain_type="stuff", 
                                                retriever=vectorstore2.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 30, "score_threshold" : score_threshold}), 
                                                return_source_documents=True, 
                                                chain_type_kwargs=chain_type_kwargs
                                                )
                    try:
                        out = qa({"query" : question})
                        print(f"---------- COS : {round(score_threshold, 2)} --------------")
                        break
                    except:
                        print("UPDATE THRESHOLD")
                        score_threshold += 0.05
    return(out)