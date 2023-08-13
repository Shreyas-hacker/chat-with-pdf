import os

from langchain import LLMChain, PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import AnalyticDB
from torch import cuda, bfloat16
import transformers

from src.helpers.Analyticdbhaidong import AnalyticDBhaidong

model_id = 'daryl149/llama-2-7b-chat-hf' # daryl149/llama-2-7b-chat-hf working but half break the vectorstore LinkSoul/Chinese-Llama-2-7b NousResearch/Nous-Hermes-llama-2-7b
# full size workding model : NousResearch/Nous-Hermes-llama-2-7b
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

# begin initializing HF items, you need an access token
hf_auth = ''
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    use_auth_token=hf_auth
)

# enable evaluation mode to allow model inference
model.eval()

print(f"Model loaded on {device}")

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

stop_list = ['\nHuman:', '\n```\n']

stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]

import torch

stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]
stop_token_ids

from transformers import StoppingCriteria, StoppingCriteriaList


# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False


stopping_criteria = StoppingCriteriaList([StopOnTokens()])

generate_text = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    # we pass model parameters here too
    stopping_criteria=stopping_criteria,  # without this model rambles during chat
    temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
    max_new_tokens=512,  # max number of tokens to generate in the output
    repetition_penalty=1.1  # without this output begins repeating
)

# from langchain.chains import ConversationalRetrievalChain

# res = generate_text("Explain me the difference between Data Lakehouse and Data Warehouse.")
# print(res[0]["generated_text"])

from langchain.embeddings import HuggingFaceEmbeddings

embeddingsllama2 = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2") # working is sentence-transformers/all-mpnet-base-v2 , trying full length embedding
# full size working embedding: sangmini/msmarco-cotmae-MiniLM-L12_en-ko-ja
from langchain.llms import HuggingFacePipeline

llmLlama2 = HuggingFacePipeline(pipeline=generate_text)

prompt = "Write a linear regression in python"
prompt_template = f'''SYSTEM: You are a helpful, respectful and honest assistant. Always answer as helpfully.

USER: {prompt}

ASSISTANT:
'''

template = """USER: {question}
ASSISTANT: Let's work this out in a step by step way to be sure we have the right answer."""
prompt = PromptTemplate(template=template, input_variables=["question"])

question = "Write a linear regression in python"
llm_chain = LLMChain(prompt=prompt, llm=llmLlama2)
print(llm_chain.run(question))



fp = "test.pdf"

ALLOW_MULTIPLE_FILES = False
ALLOWED_FILE_EXTENSION = 'pdf'
EXCERPT_LENGTH = 300
VERTICAL_SPACING = 2
NUMBER_OF_RELEVANT_CHUNKS = 2
CHAIN_TYPE = 'stuff'
WIDTH = "50"
HEIGHT = "60"

file=fp
loader = PyPDFLoader(file)
def transform_document_into_chunks(document):
    """Transform document into chunks of {1000} tokens"""
    splitter = CharacterTextSplitter(
        chunk_size=int(os.environ.get('CHUNK_SIZE', 500)),
        chunk_overlap=int(os.environ.get('CHUNK_OVERLAP', 0))
    )
    return splitter.split_documents(document)

def transform_chunks_into_embeddings(text, k , open_ai_token , adbpg_host_input, adbpg_port_input, adbpg_database_input, adbpg_user_input, adbpg_pwd_input) :
    """Transform chunks into embeddings"""
    CONNECTION_STRING = AnalyticDBhaidong.connection_string_from_db_params(
        driver=os.environ.get("PG_DRIVER", "psycopg2cffi"),
        host=os.environ.get("PG_HOST", adbpg_host_input),
        port=int(os.environ.get("PG_PORT", adbpg_port_input)),
        database=os.environ.get("PG_DATABASE", adbpg_database_input),
        user=os.environ.get("PG_USER", adbpg_user_input),
        password=os.environ.get("PG_PASSWORD", adbpg_pwd_input),
    )

    # embeddings = OpenAIEmbeddings(openai_api_key = open_ai_token)
    embeddings = embeddingsllama2

    db = AnalyticDBhaidong.from_documents(text, embeddings, connection_string=CONNECTION_STRING)
    return db.as_retriever(search_type='similarity', search_kwargs={'k': k})

chunks = transform_document_into_chunks(loader.load())
retriever = transform_chunks_into_embeddings(chunks, NUMBER_OF_RELEVANT_CHUNKS, open_ai_token="open_api_token_global",
                  adbpg_host_input="", adbpg_port_input = 5432,
                  adbpg_database_input='', adbpg_user_input='', adbpg_pwd_input='!')

# from langchain.chains import RetrievalQA
# qa = RetrievalQA.from_chain_type(
#             # llm=OpenAI(openai_api_key = open_ai_token, model_name="gpt-3.5-turbo-16k"),
#             llm=llmLlama2,
#             chain_type="stuff",
#             retriever=retriever,
#             return_source_documents=True
#         )
# query = question
# result = qa({'query': query})
# print(result)

from langchain.chains import ConversationalRetrievalChain
chat_history = []
chain = ConversationalRetrievalChain.from_llm(llmLlama2, retriever, return_source_documents=True)
query = "who is david haidong chen"
result = chain({"question": query, "chat_history": chat_history})

print(result['answer'])