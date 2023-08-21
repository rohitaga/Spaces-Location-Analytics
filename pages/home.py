# Home.py

import streamlit as st
import pandas as pd
import altair as alt
import base64
from io import BytesIO
from streamlit_extras.grid import grid

def show():
    st.title("UserCount")

    st.write("""
    This app allows you to perform an analysis on user count gathered from Cisco Spaces. After uploading your data files, 
    you can select specific dates, locations, and SSIDs to see the distinct 
    count of User Names for each combination of the selected values. The results from two files can be merged.
    """)

    # Define a grid layout
    my_grid = grid(1, [2, 1], 1, 2, vertical_align="middle")

    # Row 1
    uploaded_files = my_grid.file_uploader('Please upload one or more files.', type=['csv', 'xls', 'xlsx', 'xlsm'], accept_multiple_files=True, key="uploaded_files")
    reset_button = my_grid.button("Reset Files", key="reset_button")

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

    # Define download_button
    if uploaded_files:
        for idx, uploaded_file in enumerate(uploaded_files):
            st.write(f"## Analysis for File {idx + 1}")
            results = analyze_file(uploaded_file, use_same_filter, common_locations, common_ssids)
            st.download_button(label="Download Results as CSV", data=results.to_csv(index=False), file_name="results.csv", mime="text/csv", key=f"download_csv_{idx}")

            if idx == 0 and len(uploaded_files) > 1:
                merged_df = results
            elif len(uploaded_files) > 1:
                merged_df = pd.concat([merged_df, results]).drop_duplicates()

        if len(uploaded_files) > 1 and not merged_df.empty:
            st.write("## Merged Results")
            visualize_results(merged_df, 'Merged Files')
            st.download_button(label="Download Merged Results as CSV", data=merged_df.to_csv(index=False), file_name="merged_results.csv", mime="text/csv", key="download_merged_csv")

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

    # Create a unique key using the file name
    unique_key = f"locations_{hash(file_name)}"

    # Filter options with unique key
    locations = st.multiselect('Select Locations', options=results_df['Location Name'].unique(), key=unique_key)
    if locations:
        results_df = results_df[results_df['Location Name'].isin(locations)]

    col1, col2 = st.columns([1, 1])  # Create two columns with equal width

    col1.subheader("Table")
    col1.dataframe(results_df)  # Interactive table display

    col2.subheader("Chart")

    # Define chart title and axis labels
    chart_title = "Distinct Count of User Names Over Time"
    x_axis_label = "Local Date"
    y_axis_label = "Distinct Count of User Names"

    # Define tooltip with more human-readable labels
    tooltip = [
        alt.Tooltip('Local Date', title='Date'),
        alt.Tooltip('Location Name', title='Location'),
        alt.Tooltip('Distinct Count', title='Distinct Count of Users')
    ]

    # Create the chart with additional customization
    chart = alt.Chart(results_df).mark_line(size=3).encode(
        x=alt.X('Local Date', title=x_axis_label),
        y=alt.Y('Distinct Count:Q', title=y_axis_label),
        color='Location Name:N',
        tooltip=tooltip
    ).properties(
        title=chart_title
    ).interactive()

    col2.altair_chart(chart, use_container_width=True)

def analyze_file(file, use_same_filter=False, common_locations=None, common_ssids=None):
    df = load_data(file)

    if df is not None:
        local_dates, location_names, ssid, location_type = get_user_inputs(df, file, use_same_filter, common_locations, common_ssids)
        if local_dates and location_names and ssid:
            results_df = calculate_distinct_count(df, local_dates, location_names, ssid, location_type)
            visualize_results(results_df, file)
            return results_df

    return pd.DataFrame()