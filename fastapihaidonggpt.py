from __future__ import annotations

import os

from fastapi import FastAPI
from pydantic import BaseModel, Field
from init_llama2_13b_fast import model

prompt_template = """
<s> [INST] <<SYS>>You are an e-commerce seller who is listing a product on an e-commerce platform and required to give me the result about product in json format based on product information inputed
{”title”:””,”description":"","brand":"","category":"","variant":{"key":["value"]},"specifications":{"key":["value"]}} 
The title should not exceed 20 words. Descriptions can be based on input text with a length between 200 and 250 words. Variant should be physical attributes of product and the value of each variant can be multiple. Specifications can't be empty. <</SYS>>
"""

class User_input(BaseModel):
    query: str  = Field(
        default=prompt_template + "<|user-message|>  This is a Xiaomi 13 Ultra smartphone with 5.7 inches display of FHD resolution. It's available in space grey and black with storage from 256GB to 1TB."+"[/INST]", title="the querstion you wanna ask", max_length=300
    )

    class config:
        schema_extra = {
            "examples": [
                {
                    "query": "<|user-message|>  This is a Xiaomi 13 Ultra smartphone with 5.7 inches display of FHD resolution. It's available in space grey and black with storage from 256GB to 1TB.",

                }
            ]
        }


app = FastAPI()




@app.post("/haidonggpt_api")
def inference(input: User_input):
    ans = model(prompt_template + input.query, stream=False)
    return ans.split("{")

# pull up command: uvicorn fastapihaidonggpt:app --reload --host 0.0.0.0
