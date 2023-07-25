import base64
from io import BytesIO
import pandas as pd
import streamlit as st
import altair as alt
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Set page title and description

st.set_page_config(page_title="Data Analysis App", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")
st.title("Data Analysis App")
st.write("""
This app allows you to perform an analysis on user data. After uploading your data files, 
you can select specific dates, locations, and SSIDs to see the distinct 
count of User Names for each combination of the selected values. The results from two files can be merged.
""")

@st.cache_data
def load_data(file):
    try:
        if file.type == 'text/csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_unique_values(df, column):
    return sorted(df[column].astype(str).unique())

def get_user_inputs(df, file, use_same_filter=False, common_locations=None, common_ssids=None):
    st.sidebar.subheader(f"Settings for {file.name}")
    all_dates = get_unique_values(df, 'Local Date')
    select_all_dates = st.sidebar.checkbox(f'Select All Dates', value=True, key=f"{file.name}_all_dates")
    local_dates = all_dates if select_all_dates else st.sidebar.multiselect(f'Select Local Date(s)', all_dates, key=f"{file.name}_dates")

    if use_same_filter:
        location_names = common_locations
        ssid = common_ssids
    else:
        location_names = st.sidebar.multiselect(f'Select Location Name(s)', get_unique_values(df, 'Location Name'), key=f"{file.name}_locations")
        ssid = st.sidebar.multiselect(f'Select SSID(s)', get_unique_values(df, 'SSID'), key=f"{file.name}_ssid")

    location_type_options = get_unique_values(df, 'Location Type')
    default_location_type = "network" if "network" in location_type_options else location_type_options[0]
    location_type = st.sidebar.selectbox(f'Select Location Type', location_type_options, index=location_type_options.index(default_location_type), key=f"{file.name}_type")

    return local_dates, location_names, ssid, location_type

def calculate_distinct_count(df, local_dates, location_names, ssid, location_type):
    results_df = pd.DataFrame(columns=['Local Date', 'Location Name', 'Distinct Count'])
    for local_date in local_dates:
        for location_name in location_names:
            filtered_df = df[(df['Local Date'] == local_date) & 
                             (df['Location Name'] == location_name) & 
                             (df['Location Type'] == location_type) & 
                             (df['SSID'].isin(ssid))]

            distinct_count = filtered_df['User Name'].nunique()

            result = pd.DataFrame({'Local Date': [local_date], 'Location Name': [location_name], 'Distinct Count': [distinct_count]})
            results_df = pd.concat([results_df, result])

    results_df['Local Date'] = results_df['Local Date'].astype(str)

    return results_df

def visualize_results(results_df, file):
    file_name = file if isinstance(file, str) else file.name
    st.subheader(f"Results for {file_name}:")
    show_table = st.checkbox("Show Table", value=True, key=f"{file_name}_show_table")
    if show_table:
        st.write(results_df)

    show_chart = st.checkbox("Show Chart", value=True, key=f"{file_name}_show_chart")
    if show_chart:
        st.altair_chart(alt.Chart(results_df).mark_line().encode(
            x='Local Date:T',
            y='Distinct Count:Q',
            color='Location Name:N',
            tooltip=['Local Date', 'Location Name', 'Distinct Count']
        ).interactive(), use_container_width=True)

def download_button(df, filetype, filename):
    if filetype == "csv":
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()  # some strings <-> bytes conversions necessary here
        button_label = f"Download {filename} as CSV"
    elif filetype == "xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
        xlsx_data = output.getvalue()
        b64 = base64.b64encode(xlsx_data).decode()  # some strings <-> bytes conversions necessary here
        button_label = f"Download {filename} as XLSX"
    href = f'<a href="data:file/{filetype};base64,{b64}" download="{filename}">{button_label}</a>'
    return href

def analyze_file(file, use_same_filter=False, common_locations=None, common_ssids=None):
    df = load_data(file)

    if df is not None:
        local_dates, location_names, ssid, location_type = get_user_inputs(df, file, use_same_filter, common_locations, common_ssids)
        if local_dates and location_names and ssid:
            results_df = calculate_distinct_count(df, local_dates, location_names, ssid, location_type)
            visualize_results(results_df, file)
            return results_df

    return pd.DataFrame()

st.sidebar.image("location-analytics1.jpeg")  # Add an image to make the interface more appealing

uploaded_files = st.sidebar.file_uploader('Upload your Excel or CSV files', type=['csv', 'xls', 'xlsx', 'xlsm'], accept_multiple_files=True, key="uploaded_files")

reset_button = st.sidebar.button("Reset")
if reset_button:
    uploaded_files = []

use_same_filter = st.sidebar.checkbox('Apply the same filter to all files for Location Name and SSID')
common_locations = None
common_ssids = None

if use_same_filter and len(uploaded_files) > 0:
    sample_df = load_data(uploaded_files[0])
    if sample_df is not None:
        common_locations = st.sidebar.multiselect('Select Location Name(s) for all files', get_unique_values(sample_df, 'Location Name'), key="common_locations")
        common_ssids = st.sidebar.multiselect('Select SSID(s) for all files', get_unique_values(sample_df, 'SSID'), key="common_ssids")

if len(uploaded_files) > 0:
    if len(uploaded_files) == 1:
        st.write(f"## Analysis for File 1")
        results = analyze_file(uploaded_files[0], use_same_filter, common_locations, common_ssids)
        if not results.empty:
            st.markdown(download_button(results, 'csv', 'results.csv'), unsafe_allow_html=True)
            st.markdown(download_button(results, 'xlsx', 'results.xlsx'), unsafe_allow_html=True)
    else:
        for idx, uploaded_file in enumerate(uploaded_files):
            st.write(f"## Analysis for File {idx + 1}")
            results = analyze_file(uploaded_file, use_same_filter, common_locations, common_ssids)

            if idx == 0:
                merged_df = results
            else:
                merged_df = pd.concat([merged_df, results]).drop_duplicates()

        if not merged_df.empty:
            st.write("## Merged Results")
            visualize_results(merged_df, 'Merged Files')

            st.markdown(download_button(merged_df, 'csv', 'merged_results.csv'), unsafe_allow_html=True)
            st.markdown(download_button(merged_df, 'xlsx', 'merged_results.xlsx'), unsafe_allow_html=True)
else:
    st.write('Please upload one or more files.')

# Display app gallery

st.write("## App Gallery")
st.write("Check out some of our favorite apps created by Streamlit users and hosted on Streamlit Community Cloud.")
st.write("Try them out, browse their source code, share with the world, and get inspired for your own projects 🤩")
st.write("Want to build your own? Get started today!")
st.write("[Streamlit App Gallery](https://streamlit.io/gallery)")

# Display API reference

st.write("## API Reference")
st.write("Streamlit makes it easy for you to visualize, mutate, and share data. The API reference is organized by activity type, like displaying data or optimizing performance.")
st.write("Each section includes methods associated with the activity type, including examples. Browse our API below and click to learn more about any of our available commands! 🎈")
st.write("[Streamlit API Reference](https://docs.streamlit.io/library/api-reference)")
