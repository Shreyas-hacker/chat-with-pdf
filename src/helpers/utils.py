from __future__ import annotations

import pprint
from tempfile import NamedTemporaryFile
from typing import Any
import streamlit as st
from init_llama2_13b_fast import model

my_openai_api_key = 'something'





def get_text():
    """Get text from user"""
    input_text = st.text_input("You: ")
    return input_text


def generate_response(query: str) -> dict[str, Any]:

    if query == "who are you":
        result_content = """I am HD C """
        result = {'query': query, 'result': result_content}
        return result
    else:

        chat_history = []

        result = model(query, stream=False)
        pprint.pprint(result)

    return {"answer":result}





