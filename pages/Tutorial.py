# tutorial.py

import streamlit as st

def show():
    st.title("Tutorial")
    
    st.write("""
    ## How to Use This Application
    
    1. **Upload Your Data**: Click the 'Upload your Excel or CSV files' button in the sidebar. You can upload one or more files at once. The files should be in either CSV or Excel format.
    2. **Select Filters**: Depending on the uploaded files, you can select specific dates, locations, SSIDs, and location types. These options are available in the sidebar.
    3. **View Results**: After setting your preferences, the application will calculate the distinct count of User Names for each combination of the selected values. The results will be displayed both in a table and a line chart.
    4. **Download Results**: If you want to download the results, you can do so in either CSV or Excel format. The download links are located under the results table and chart.
    5. **Reset**: If you want to start over, click the 'Reset' button in the sidebar.
    
    ## Troubleshooting
    
    If you encounter any issues while using this application, try the following:
    
    - Ensure your data files are in the correct format (CSV or Excel).
    - If the application seems stuck, try clicking the 'Reset' button in the sidebar.
    - If all else fails, try refreshing the page.

    ## Contact
    
    If you need further assistance, please drop an email.
    """)
