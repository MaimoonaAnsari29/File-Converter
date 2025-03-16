import streamlit as st
import pandas as pd
from io import BytesIO

# Set the page configuration
st.set_page_config(page_title="DATA SWEEPER", layout="wide")
st.title("DATA SWEEPER")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader to allow user to upload CSV or Excel files
files = st.file_uploader("Upload CSV or EXCEL Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        # Detect file extension and load the corresponding data
        ext = file.name.split(".")[-1].lower()
        
        # Read the file based on its extension
        if ext == "csv":
            df = pd.read_csv(file)
        elif ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type!")
            continue
        
        # Display the first few rows of the data
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())
        
        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())
        
        # Fill Missing values with Mean (for numeric columns)
        if st.checkbox(f"Fill Missing values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with mean")
            st.dataframe(df.head())
        
        # Select Columns to Display
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())
        
        # Show chart for numerical data (if available)
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])  # Display first 2 numerical columns
        
        # Convert file format
        format_choice = st.radio(f"Convert {file.name} to:", ["None", "CSV", "Excel"], key=file.name)
        
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            elif format_choice == "Excel":
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            else:
                st.warning("Please select a valid format to convert.")
                continue
            
            # Move the pointer to the beginning of the BytesIO buffer
            output.seek(0)
            
            # Provide the download button
            st.download_button(
                label=f"Download {new_name}",
                data=output,
                file_name=new_name,
                mime=mime
            )
            
            st.success("Processing Complete!")
