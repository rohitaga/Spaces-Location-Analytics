# APIPage.py

import streamlit as st

def show():
    # Display the content from the "API Reference" section
    st.write("## API Reference")
    st.write("""
    Streamlit makes it easy for you to visualize, mutate, and share data. The API reference is organized by activity type, like displaying data or optimizing performance.
    Each section includes methods associated with the activity type, including examples. Browse their API below and click to learn more about any of their available commands! 🎈
    """)
    st.write("[Streamlit API Reference](https://docs.streamlit.io/library/api-reference)")

    # Display the content from the "App Gallery" section
    st.write("## App Gallery")
    st.write("""
    Check out some of their favorite apps created by Streamlit users and hosted on Streamlit Community Cloud.
    Try them out, browse their source code, share with the world, and get inspired for your own projects 🤩
    Want to build your own? Get started today!
    """)
    st.write("[Streamlit App Gallery](https://streamlit.io/gallery)")
    