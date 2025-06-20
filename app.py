import  streamlit as st
from streamlit.runtime.state import session_state
import utils 

st.set_page_config(page_title="ChatBot Basico", 
                    page_icon="☣️",
                    layout="wide"
                    )

st.title("ChatBot Basico 199")


#creacion de una memoria cache que guarde 
#el contexto sobre la tematica que se esta hablando

if "history" not in st.session_state: 
    st.session_state.history = []
    #cookies para guardar datos temporales


#PARA EL CONTEXTO
if "coontext" not in st.session_state:
    st.session_state.context = []


#construimos el espacio, emisor-mensaje
#creacion de un ciclo que se este rrecoriendo constantemente
#como el historial

for sender, msg in st.session_state.history:
    if sender =="Tú":
        st.markdown(f'**⛹️‍♂️☁ {sender}:**{msg}')
    else:
        st.markdown(f'**🤖{sender}:**{msg}')


#si no hay entrada

if "user_input" not in st.session_state:
    st.session_state.user_input=""



#procesamiento de la entrada
def send_msg():
    user_input =st.session_state.user_input.strip()
    if user_input:
        tag = utils.predict_class(user_input)
        st.session_state.context.append(tag)
        response=utils.get_response(tag, st.session_state.context)
        st.session_state.history.append(('Tú', user_input))
        st.session_state.history.append(('Bot',response))
        session_state.user_input=""


#Creamos el campo

st.text_input("Escribe tu mensaje:", 
                key="user_input",
                on_change= send_msg)