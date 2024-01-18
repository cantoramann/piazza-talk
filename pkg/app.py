import streamlit as st

st.title('Piazza Talk')
st.header('Your Class Data Dashboard')

classes_tab, envs_tab = st.tabs(["Classes", "Environment Variables"])
with classes_tab:
    'This is tab1'
with envs_tab:
    'This is tab2'
    with st.sidebar:
            st.write('sidebar')