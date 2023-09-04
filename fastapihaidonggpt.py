from __future__ import annotations

import os

from fastapi import FastAPI
from pydantic import BaseModel,Field
from init_llama2_13b_fast import model
class User_input(BaseModel):
    query: str | None = Field(
        default="who is david haidong chen", title="the querstion you wanna ask", max_length=300
    )

    class config:
        schema_extra = {
            "examples": [
                {
                    "query": """<|bot|> give me the result about product on e-commerence platform in json format based on product information inputed.

{\"title\":\"\",\"description\":\"\",\"brand\":\"\",\"category\":\"\",\"variant\":{\"color\":[\"Space Grey\“,\”black\“]},\”specifications\”:{\”display\”:[\”5.7 inches\”]}} 

The title should not exceed 20 words and contain the main features and uses. descriptions can be based on input text and your own knowledge base, with a length between 200 and 250 words. variant should be physical attributes of product and the value of each variant can be multiple specifications like size of screen of a phone.
<|user-message|> This is a Xiaomi 13 Ultra smartphone with 5.7 inches display of FHD resolution. It's available in space grey and black with storage from 256GB to 1TB.
""",

                }
            ]
        }


app = FastAPI()

@app.post("/haidonggpt_api")
def inference(input:User_input):
    return model(input.query, stream=False)

# pull up command: uvicorn fastapihaidonggpt:app --reload --host 0.0.0.0