import streamlit as st

st.write(
    """
   # Sample Streamlit App
"""
)

with st.form(key="my_form"):
    st.write("This is a form with a text input and a submit button.")
    text_input = st.text_input("Enter some text:")
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.write(f"You entered: {text_input}")
        st.balloons()
        st.success("Form submitted successfully!")
