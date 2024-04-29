import streamlit as st

st.title('Request a Consultation')

with st.form(key='contact_form'):
    name = st.text_input('Name')
    email = st.text_input('Email')
    message = st.text_area('Message')
    submit_button = st.form_submit_button('Submit')

    if submit_button:
        st.success('Thank you for contacting us. We will get back to you shortly.')