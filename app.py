# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup our app
st.set_page_config(page_title="💿💾 Data Sweeper", layout='wide')
st.title("💿💾 Data Sweeper")
st.write("Transform your files b/w CSV and Excel formats with built-in cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:  # type: ignore
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
            st.write(f"**Preview of CSV file {file.name}:**")
            st.dataframe(df.head())
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
            st.write(f"**Preview of Excel file {file.name}:**")
            st.dataframe(df.head())
        else:
            st.error(f"File type should be .csv or .xlsx. You uploaded a {file_ext} file.")
            continue

        #Display Info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        #shows 5 rows of our df
        st.write("preview the head of dataframe")
        st.dataframe(df.head())

        #Data cleaning options
        st.subheader("🛠️Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                    if st.button(f"Please input Missing Values for{file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing Values have been Filled!")

        #Choose specific column to keep or convert
        st.subheader("Select a Column to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default= df.columns)
        df = df[columns]

        #create some visualizations
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include= 'number').iloc[:, :2])


        #Convert the file CSV -> Excel
        st.subheader("🔄️ Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 Files Processed!")
