import streamlit as st
from openai import OpenAI
import re
import time

st.set_page_config(page_title="Chat Loggi", page_icon="📖", layout="wide")

st.title("💬 Logger Virtual")


API_KEY = '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'
id_assistant = 'asst_nYvqra8wrtHg20FlQTcfC7EC'

def inicializa_open_ai():
    client = assistant = thread = None
    try:
        client = OpenAI(api_key='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')
        assistant = client.beta.assistants.retrieve(id_assistant)
        thread = client.beta.threads.create()
        return client, assistant, thread
    except:
        return client, assistant, thread


def envia_msg(client, assistant, thread, mensagem):
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mensagem
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    run_id = run.id
    structured_response=[]
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run_id
        )
        
        if run_status.status == "completed":
            resposta =client.beta.threads.messages.list(
                thread_id=thread.id
            )
            break
        elif run_status.status in ['queued', 'in_progress']:
            print(f'{run_status.status.capitalize()}... Please wait.')
            time.sleep(1)  # Wait before checking again
        else:
            print(f"Run status: {run_status.status}")
            break
    return resposta.data[0].content[0].text.value

client, assistant, thread = inicializa_open_ai()
if client is not None:
    st.session_state['client'] = client
if assistant is not None:
    st.session_state['assistant'] = assistant

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Olá, sou o Logger Virtual, como posso ajudar você?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = envia_msg(client, assistant, thread, prompt)
    msg = re.sub(r"【.*?】", '', msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)