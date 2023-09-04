import base64
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from config.default import config
from src.helpers.utils import  generate_response
import os
open_api_token_global = ""
def create_app(config_name):
    """Create a streamlit app"""
    cf = config[config_name]
    st.set_page_config(page_title='haidongGPT for DoctorGPT',
                       page_icon='🤖', layout='centered', initial_sidebar_state='auto')
    st.header(cf.TITLE)


    # we need a way to remember the chat history
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    if 'generated' not in st.session_state:
        st.session_state.generated = []
    if 'past' not in st.session_state:
        st.session_state.past = []
    if 'source' not in st.session_state:
        st.session_state.source = []

    """
    *---------------------------------------*-----------------------------------------------------*
    *---------------------------------------*-----------------------------------------------------*
                                  ****Utility method****
    """
    def submit():
        st.session_state.user_input = st.session_state.widget
        st.session_state.widget = ''

    def excerpt(text, n=cf.EXCERPT_LENGTH):
        return text[:n] + '...' if len(text) > n else text
    """
    *---------------------------------------*-----------------------------------------------------*
    *---------------------------------------*-----------------------------------------------------*
    """


    if True:
        # show the pdf thumbnail :-)

        response_container = st.container()

        st.text_input('🤖 666 👋🏾, Ask me anything', key='widget', on_change=submit)
        with response_container:
            if st.session_state.user_input:
                response = generate_response(st.session_state.user_input)

                st.session_state.past.append(st.session_state.user_input)
                st.session_state.generated.append(response['answer'])
            if st.session_state.generated:
                for i in range(len(st.session_state.generated)):
                    message(st.session_state.past[i], is_user=True, key=str(i) + '_user', avatar_style='micah')
                    message(st.session_state.generated[i], key=str(i))
                    if st.session_state.source:
                        with st.expander(':blue[See references]'):
                            st.markdown(st.session_state.source[i], unsafe_allow_html=True)
