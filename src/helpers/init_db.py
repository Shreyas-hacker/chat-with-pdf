
import os
import cassio

token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
database_id = os.getenv("ASTRA_DB_ID")

cassio.init(token=token, database_id=database_id)

from langchain.embeddings import OpenAIEmbeddings
emb_fun = OpenAIEmbeddings(openai_api_key = os.getenv("OPENAI_API_KEY"))


v_store = cassio.table.VectorCassandraTable(table="demo_v_store", vector_dimension=1536)

docs = [
    "The cat is on the table",
    "Please store the appliance safely when not using it",
    "All happy families are alike, each unhappy family is unhappy in its own way",
]

for i, txt in enumerate(docs):
    v_store.put(row_id=f"row{i}", body_blob=txt, vector=emb_fun.embed_query(txt))
    print(f"Inserted '{txt}'")

query = "Is a feline found around here?"

results = v_store.ann_search(n=1, vector=emb_fun.embed_query(query))

print(f"Query: '{query}'")
print("Result(s):")
for r in results:
    print(f"    [{r['row_id']}]: '{r['body_blob']}'")

