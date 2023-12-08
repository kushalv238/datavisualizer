import streamlit as st
import pandas as pd
import datetime

if 'log_entries' not in st.session_state:
    st.session_state.log_entries = []
    
def log_entry(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.log_entries.append(f"{timestamp}:\t\t {message}")

def load_data():
    uploaded_files = st.file_uploader("Upload datasets", type=["csv", "xlsx"], accept_multiple_files=True)
    
    datasets = []
    dataset_names = []
    
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)  # You can also handle Excel files if needed
            datasets.append(df)
            dataset_names.append(uploaded_file.name)
            log_entry(f"Dataset '{uploaded_file.name}' with {df.shape[0]} rows and {df.shape[1]} columns has been uploaded.")
        except Exception as e:
            log_entry(f"Dataset '{uploaded_file.name}' uploading failed")
            st.error(f"Error loading dataset: {e}")
            
    return datasets, dataset_names

def show_plots(df):
    st.subheader("Data Visualization")
    
    plot_type = st.selectbox("Select a plot type", ["Line Chart", "Bar Chart", "Scatter Plot"])
    selected_column = st.selectbox("Select column", df.columns)

    try:
        if plot_type == "Line Chart":
            st.line_chart(df[selected_column])
        elif plot_type == "Bar Chart":
            st.bar_chart(df[selected_column].value_counts())
        elif plot_type == "Scatter Plot":
            comparision_column = st.selectbox("Select second column", df.columns)
            st.scatter_chart(df[[selected_column, comparision_column]])
        # Add more plot types as needed
        else:
            st.warning("Selected plot type is not supported.")
    except Exception as e:
        st.error(f"Error generating visualization: {e}")
 
def show_data_analysis(df):
    st.subheader("Data Analysis")
 
    selected_columns = st.multiselect("Select columns for analysis", df.columns)
    if selected_columns:
        st.write("Descriptive Statistics")
        st.write(df[selected_columns].describe())
 
def data_opns(df):
    st.subheader("Data Analysis")
 
    # OLAP-like operations
    operation = st.selectbox("Select an OLAP operation", ["Group By", "Aggregate", "Slice and Dice", "Pivot"])

    if operation == "Group By":
        group_columns = st.multiselect("Select columns for grouping", df.columns)
        if group_columns:
            grouped_df = df.groupby(group_columns).size().reset_index(name='Count')
            st.write("Grouped Data:")
            st.write(grouped_df)

    elif operation == "Aggregate":
        numeric_columns = df.select_dtypes(include='number').columns

        if len(numeric_columns) == 0:
            st.warning("No numeric columns found for aggregation.")
        else:
            aggregation = st.selectbox("Select an aggregation function", ["mean", "median", "sum", "count"])

            aggregated_data = {}

            for column in numeric_columns:
                if aggregation == "mean":
                    result = df[column].mean()
                elif aggregation == "sum":
                    result = df[column].sum()
                elif aggregation == "count":
                    result = df[column].count()
                elif aggregation == "median":
                    result = df[column].median()

                aggregated_data[f"{column}_{aggregation}"] = result

            st.write("Aggregated Data:")
            st.write(pd.Series(aggregated_data))


    elif operation == "Slice and Dice":
        slice_column = st.selectbox("Select a column for slicing", df.columns)
        slice_value = st.text_input("Enter value for slicing:")
        sliced_df = df[df[slice_column] == slice_value]
        st.write("Sliced Data:")
        st.write(sliced_df)

    elif operation == "Pivot":
        st.subheader("Pivot")
        pivot_index = st.selectbox("Select an index column for pivoting", df.columns)
        pivot_columns = st.multiselect("Select columns for pivoting", df.columns)
        pivot_values = st.selectbox("Select values column for pivoting", df.columns)
        pivot_table = pd.pivot_table(df, values=pivot_values, index=pivot_index, columns=pivot_columns, aggfunc='mean')
        st.write("Pivoted Data:")
        st.write(pivot_table)
        
def show_logs():
    st.subheader("Log Page")
    for entry in st.session_state.log_entries:
        st.write(entry)
 
def main():
    st.title("DataVisualizer")
    
    contributers = ["Kushal Vadodaria - 60003210188", "Isha Mistry - 60003210197", "Kely Mistry - 60003210197"]
    st.markdown("### Project contributers:")
    st.markdown("\n".join([f"- {item}" for item in contributers]))
    
    st.write("Upload datasets and navigate to other pages for analysis.")


    datasets, dataset_names = load_data()

    if datasets:
        selected_dataset = st.sidebar.selectbox("Select a dataset", dataset_names)

        df = datasets[dataset_names.index(selected_dataset)]

        page = st.sidebar.radio("Select a page", ["Home", "Data Visualization", "Data Analysis","Data Operations", "Log Page"])
 
        if page == "Home":
            st.markdown(f"<p style='font-size: 2.5rem; text-decoration: underline;'>{selected_dataset}</p>", unsafe_allow_html=True)
            st.write(df)
        elif page == "Data Visualization":
            show_plots(df)
        elif page == "Data Analysis":
            show_data_analysis(df)
        elif page == "Data Operations":
            data_opns(df)
        elif page == "Log Page":
            show_logs()
 
if __name__ == "__main__":
    main()