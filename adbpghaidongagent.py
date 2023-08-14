import os

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

import init_llama2_medium
from src.helpers.Analyticdbhaidong import AnalyticDBhaidong

connectionstring = AnalyticDBhaidong.connection_string_from_db_params(
    driver=os.environ.get("PG_DRIVER", "psycopg2cffi"),
    host=os.environ.get("PG_HOST", "adbpg_host_input"),
    port=int(os.environ.get("PG_PORT", "adbpg_port_input")),
    database=os.environ.get("PG_DATABASE", "adbpg_database_input"),
    user=os.environ.get("PG_USER", "adbpg_user_input"),
    password=os.environ.get("PG_PASSWORD", "adbpg_pwd_input"),
)

db = SQLDatabase.from_uri(connectionstring)
toolkit = SQLDatabaseToolkit(db=db, llm=llmLlama2)

agent_executor = create_sql_agent(
    llm=llmLlama2,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)



agent_executor.run("Describe the playlisttrack table")
