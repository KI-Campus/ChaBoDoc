import streamlit as st
import nltk
import os

import pandas as pd

from models import Netpicker

#from utils import Classifier
#import matplotlib

@st.cache(suppress_st_warning=True)
def download_punkt():
    nltk.download("punkt")

# ---------------------------------------------------------------------------------------------------------

def app():
    st.markdown("## 5. Vergleich der ChatBots")

    st.markdown(
        "Hier können die ChatBots verschiedener Gruppen geladen und getestet werden."
    )

    st.markdown("---")

    # TODO read group names from some file or anything similar
    group_list_dropdown = ["Melinda", 
                            "Salzwerk", 
                            "Gruppe", 
                            "MarzInator", 
                            "LuSo", 
                            "Frankensteinmonster", 
                            "Supernet", 
                            "Mogelnet"
                        ]

    chatbot_option = st.selectbox(
        "ChatBot Auswahl",
        group_list_dropdown, 
    )

    # TODO take Gruppe(...) instead of Testgruppe
    print("Loading", chatbot_option)
    current_group = Netpicker(chatbot_option)

    table_current_group_input = chatbot_option + "user_table_entries"
    table_current_group_good = chatbot_option + "good_table_entries"
    table_current_group_bad = chatbot_option + "bad_table_entries"
    table_current_group_neutral = chatbot_option + "neutral_table_entries"
    if table_current_group_input not in st.session_state:
        #st.write("Group not in session state")
        st.session_state[table_current_group_input] = []
        st.session_state[table_current_group_good] = []
        st.session_state[table_current_group_bad] = []
        st.session_state[table_current_group_neutral] = []

    st.markdown("---")

    st.markdown("Chatbot ("+current_group.name+"): Wie geht es dir heute?")

    with st.form("user_input", clear_on_submit=True):
        user_input = st.text_input("Nutzer:", key="input_sentence")
        submit = st.form_submit_button(label="Senden")

    st.markdown("---")

    if submit:
        result = current_group.predict(user_input)

        st.session_state[table_current_group_input].append(user_input)
        st.session_state[table_current_group_good].append(result[1].item())
        st.session_state[table_current_group_bad].append(result[0].item())
        st.session_state[table_current_group_neutral].append(result[2].item())

        st.markdown("Details zu Antwort")
        result_table = {
            "Nutzer": st.session_state[table_current_group_input],
            "gut": st.session_state[table_current_group_good],
            "schlecht": st.session_state[table_current_group_bad],
            "neutral": st.session_state[table_current_group_neutral],
        }

        result_table = pd.DataFrame.from_dict(result_table)

        st.table(result_table.style.background_gradient(axis=None, cmap="Blues"))

    #st.sidebar.image("./images/Logo_Uni_Luebeck_600dpi.png", use_column_width=True)
    #st.sidebar.image("./images/Logo_UKT.png", use_column_width=True)
