from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel, Field
from init_llama2_medium import gen_sentiment


class User_input(BaseModel):
    query: str | None = Field(
        default='''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
Input: FINANCING OF ASPOCOMP 'S GROWTH Aspocomp is aggressively pursuing its growth strategy by increasingly focusing on technologically more demanding HDI printed circuit boards PCBs .
Answer: ''', title="the finanical news you want to know postive neg or netual", max_length=300
    )

    class config:
        schema_extra = {
            "examples": [
                {
                    "query": '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
Input: FINANCING OF ASPOCOMP 'S GROWTH Aspocomp is aggressively pursuing its growth strategy by increasingly focusing on technologically more demanding HDI printed circuit boards PCBs .
Answer: ''',

                }
            ]
        }


app = FastAPI()


@app.post("/haidonggpt_api")
def inference(input: User_input):
    return gen_sentiment(input)

# pull up command: uvicorn fastapihaidonggpt:app --reload --host 0.0.0.0
