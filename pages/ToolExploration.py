import streamlit as st

def show():
    st.title("Tool Exploration")

    tool = st.selectbox("Choose a tool", ["Pandas", "Streamlit", "Altair", "Numpy"])

    if tool == "Pandas":
        st.write("""
        ## Pandas

        Pandas is a software library written for the Python programming language for data manipulation and analysis. 
        Here are some tips and tricks:

        1. **Method Chaining**: Pandas methods return DataFrames, so it's easy to chain methods together. For example: `df.isnull().sum()`
        2. **Handling Missing Values**: Use `df.fillna()` to fill missing values with a specific value or method (like 'mean'). Use `df.dropna()` to remove rows with missing values.
        3. **`groupby` Magic**: The `groupby` function is extremely powerful. After calling `df.groupby('column')`, you can do things like `.mean()` or `.count()` to get the mean or count of each group.
        """)

    elif tool == "Streamlit":
        st.write("""
        ## Streamlit

        Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. 
        Here are some tips and tricks:

        1. **Caching**: Use `@st.cache_data` to cache the results of long-running computations, dramatically speeding up your app.
        2. **Magic**: Streamlit has 'magic' commands that let you write less code. For example, you can display a variable by just writing its name.
        3. **Widgets**: Streamlit has many built-in widgets like `st.slider`, `st.selectbox`, and `st.multiselect` for interactive apps.
        """)

    elif tool == "Altair":
        st.write("""
        ## Altair

        Altair is a declarative statistical visualization library for Python. 
        Here are some tips and tricks:

        1. **Interactivity**: You can easily make your Altair charts interactive with the `.interactive()` method.
        2. **Tooltips**: Add tooltips to your chart with the `tooltip` encoding. This lets users hover over points to get more information.
        3. **Save Charts**: You can save Altair charts as HTML or JSON with the `chart.save('filename.html')` method.
        """)

    elif tool == "Numpy":
        st.write("""
        ## Numpy

        Numpy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays. 
        Here are some tips and tricks:

        1. **Broadcasting**: Numpy can do element-wise operations on arrays of different shapes by 'broadcasting' the smaller array across the larger one.
        2. **Vectorization**: Numpy functions can operate on whole arrays at once, making your code faster and more readable.
        3. **Random Numbers**: Use `np.random` to generate arrays of random numbers, or to shuffle an array.
        """)

    st.write("Explore more about ", tool, " and boost your data analysis tasks.")