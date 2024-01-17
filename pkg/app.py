import streamlit as st

st.title('Piazza Talk')
st.header('Your Class Data Dashboard')

tab1, tab2, tab3 = st.tabs(["Classes", "Environment Variables"])
with tab1:
    'This is tab1'
with tab2:
    'This is tab2'
    with st.sidebar:
            st.write('sidebar')
with tab3:
    'This is tab3'


# if st.button('Add Class'):
#     with st.form(key='add_class_form'):
#         class_name = st.text_input('Class Name')
#         class_id = st.text_input('Class ID')
#         instructor = st.text_input('Instructor Name')
#         submit_button = st.form_submit_button(label='Submit')


# list_of_classes = ['CS 101', 'CS 102', 'CS 103']
# selected_class = st.sidebar.selectbox('Select a Class', list_of_classes)

# def display_class_dropdown(classes):
#     selected_class = st.selectbox("Select a Class", classes)
#     return selected_class

# if __name__ == "__main__":
#     class_names = load_class_names('path/to/your/classes.txt')  # Update with the correct path
#     if class_names:
#         selected_class = display_class_dropdown(class_names)
#         st.write(f"You selected: {selected_class}")
#     else:
#         st.error('No classes found.')
