import base64
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from config.default import config
from src.helpers.utils import get_text, setup, get_file_path, generate_response
import os
open_api_token_global = ""
def create_app(config_name):
    """Create a streamlit app"""
    cf = config[config_name]
    st.set_page_config(page_title='haidongGPT for DoctorGPT',
                       page_icon='🤖', layout='centered', initial_sidebar_state='auto')
    st.header(cf.TITLE)

    open_api_token_global = "something"
    # open_api_token_global = st.text_input('your openai token', 'something')
    # st.write('The current chatgpt api token is', open_api_token_global)

    #  adbpg_user_input, adbpg_pwd_input
    # # Returns `None` if the key doesn't exist
    # print(os.environ.get('KEY_THAT_MIGHT_EXIST'))
    # conn_string = os.environ.get('PG_HOST', '')
    # conn_port = os.environ.get('PG_PORT', '')
    # adbpg_database = os.environ.get('PG_DATABASE', '')
    # adbpg_user = os.environ.get('PG_USER', '')
    # adbpg_passwd = os.environ.get('PG_PASSWORD', '')

    # adbpg_host_input_global = ""
    # adbpg_port_input_global = ""
    # adbpg_database_input_global = ""
    # adbpg_user_input_global = ""
    # adbpg_pwd_input_global = ""

    # adbpg_host_input_global = st.text_input('your adbpg_host', conn_string)
    # st.write('The current adbpg_host_input', adbpg_host_input_global)
    # adbpg_port_input_global = st.text_input('your adbpg_port', conn_port)
    # st.write('The current adbpg_port is', adbpg_port_input_global)
    # adbpg_database_input_global = st.text_input('your adbpg_database', adbpg_database)
    # st.write('The current adbpg_database is', adbpg_database_input_global)
    # adbpg_user_input_global = st.text_input('your adbpg_user', adbpg_user)
    # st.write('The current adbpg_user is', adbpg_user_input_global)
    # adbpg_pwd_input_global = st.text_input('your adbpg_pwd', adbpg_passwd)
    # st.write('The current adbpg_pwd is', adbpg_pwd_input_global)

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

    # def show_pdf(file_path):
    #     with open(file_path, "rb") as f:
    #         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    #         pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={cf.WIDTH} ' \
    #                       f'height={cf.HEIGHT} type="application/pdf"></iframe>'
    #         st.markdown(pdf_display, unsafe_allow_html=True)

    def excerpt(text, n=cf.EXCERPT_LENGTH):
        return text[:n] + '...' if len(text) > n else text
    """
    *---------------------------------------*-----------------------------------------------------*
    *---------------------------------------*-----------------------------------------------------*
    """

    # let the user upload a pdf or txt file
    # pdf = st.file_uploader(
    #     'Upload a PDF file',
    #     type=[ext for ext in cf.ALLOWED_FILE_EXTENSION.split(',')],
    #     accept_multiple_files=cf.ALLOW_MULTIPLE_FILES,
    #     label_visibility='hidden'
    # )
    if True:
        # show the pdf thumbnail :-)

        response_container = st.container()
        # processing start here...
        # s = setup(file=fp, number_of_relevant_chunk=cf.NUMBER_OF_RELEVANT_CHUNKS, open_ai_token=open_api_token_global,
        #           adbpg_host_input=adbpg_host_input_global, adbpg_port_input = adbpg_port_input_global,
        #           adbpg_database_input=adbpg_database_input_global, adbpg_user_input=adbpg_user_input_global, adbpg_pwd_input=adbpg_pwd_input_global)
        st.text_input('🤖 666 👋🏾, Ask me anything', key='widget', on_change=submit)
        with response_container:
            if st.session_state.user_input:
                response = generate_response(st.session_state.user_input)
                if response['source_documents']:
                    all_refs = ''
                    for doc in response['source_documents']:
                        content = excerpt(doc.page_content)
                        page = doc.metadata.get('page')
                        ref = f"""
                        *{content}*
                        \n☝🏽#{page} 📖\n
                        """
                        all_refs += ref
                    st.session_state.source.append(all_refs)
                st.session_state.past.append(st.session_state.user_input)
                st.session_state.generated.append(response['answer'])
            if st.session_state.generated:
                for i in range(len(st.session_state.generated)):
                    message(st.session_state.past[i], is_user=True, key=str(i) + '_user', avatar_style='micah')
                    message(st.session_state.generated[i], key=str(i))
                    if st.session_state.source:
                        with st.expander(':blue[See references]'):
                            st.markdown(st.session_state.source[i], unsafe_allow_html=True)
