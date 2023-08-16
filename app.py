import base64
from io import BytesIO
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import altair as alt
import warnings
from pages import ToolExploration, TrustandSecurity, Tutorial, APIPage
from pages.home import show as show_home
from PIL import Image

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Set the page config once at the start of your main script
st.set_page_config(page_title="UserCount", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

# Remove the Streamlit generated page components on the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# st.sidebar.image("location-analytics1.jpeg")  # Add an image to make the interface more appealing

selected = option_menu(
          menu_title=None,  # required
          options=["Home", "Tutorial", "API Page", "Tool Exploration", "Trust and Security"],
          icons=["house", "book", "code", "tools", "envelope"],
          menu_icon="cast",  # optional
          default_index=0,  # optional
          orientation="horizontal",
     )

# Navigation
if selected == "Home":
    image = Image.open('location-analytics1.jpeg')
    st.sidebar.image(image, caption='Location Analytics')
    show_home()
    # Rest of the code for the "Home" page

elif selected == "Tutorial":
    image = Image.open('location-analytics2.jpeg')
    st.sidebar.image(image, caption='Location Analytics')
    Tutorial.show()
    # Rest of the code for the "Tutorial" page

elif selected == "API Page":
    image = Image.open('location-analytics3.png')
    st.sidebar.image(image, caption='Location Analytics')
    APIPage.show()
    # Rest of the code for the "API Page" page

elif selected == "Tool Exploration":
    image = Image.open('location-analytics4.jpeg')
    st.sidebar.image(image, caption='Location Analytics')
    ToolExploration.show()
    # Rest of the code for the "Tool Exploration" page

elif selected == "Trust and Security":
    image = Image.open('location-analytics5.jpeg')
    st.sidebar.image(image, caption='Location Analytics')
    TrustandSecurity.show()