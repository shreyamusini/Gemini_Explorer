import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'astute-dreamer-413322'
vertexai.init(project = project)
config = generative_models.GenerationConfig(
    temperature = 0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
chat = model.start_chat()

st.title("Gemini Explorer") 
user_name = st.text_input("What is your name? ")
weather_location = st.text_input("What is your location? ")

#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {"role" : "user", 
        "content" : query 
        }
    )
    st.session_state.messages.append(
        {
            "role" : "model",
            "content" : output
        }
    )

#initializing chat history 
# if nothing passed, the session is empty 
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display and Load Chat History
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )

    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)

# Initial message startup - first message from chat
if len(st.session_state.messages) == 0:
    # st.write(personal_greeting)
    if weather_location and user_name:
        initial_message = f"Greet the user using the information in {user_name} and introduce yourself as ReX, an \
        assistant powered by Google Gemini. Be interactive by using emojis. Use the information in {weather_location} to then \
        tell the user a fun fact about their location"
        llm_function(chat, initial_message)
    # llm_function(chat, personal_greeting)

if user_name:
    if weather_location:
        query = st.chat_input("Gemini Explorer")
        if query:
            with st.chat_message("user"):
                st.markdown(query)
            llm_function(chat, query)
