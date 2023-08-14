import os

from fastapi import FastAPI
from pydantic import BaseModel
from src.helpers.utils import get_text, setup, get_file_path, generate_response
class User_input(BaseModel):
    query: str
    file_path: str


app = FastAPI()

@app.post("haidonggpt_api")
def inference(input:User_input):
    NUMBER_OF_RELEVANT_CHUNKS = 2
    CHAIN_TYPE = 'stuff'
    host = os.environ.get("PG_HOST", "adbpg_host_input"),
    port = int(os.environ.get("PG_PORT", "adbpg_port_input")),
    database = os.environ.get("PG_DATABASE", "adbpg_database_input"),
    user = os.environ.get("PG_USER", "adbpg_user_input"),
    password = os.environ.get("PG_PASSWORD", "adbpg_pwd_input")
    s = setup(file=input.file_path, number_of_relevant_chunk=NUMBER_OF_RELEVANT_CHUNKS, open_ai_token="",
              adbpg_host_input=host, adbpg_port_input=port,
              adbpg_database_input=database, adbpg_user_input=user,
              adbpg_pwd_input=password)
    return generate_response(input.query,chain_type=CHAIN_TYPE,retriever=s,open_ai_token="")

# uvicorn fastapihaidonggpt:app --reload --host 0.0.0.0