import streamlit as st
import pandas as pd
from io import BytesIO

# Set up the Streamlit page
st.set_page_config(page_title="File Converter & Cleaner", layout="wide")
st.title("📁 File Converter & Cleaner")
st.write("Upload your CSV or Excel files to clean the data and convert formats effortlessly.")

# File uploader
files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # File preview
        st.subheader(f"📄 {file.name} - Preview")
        st.data_editor(df.head())

        # Fill missing values
        if st.checkbox(f"🧹 Fill Missing Values - {file.name}"):
            numeric_cols = df.select_dtypes(include="number").columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success("✅ Missing values filled successfully!")
            st.dataframe(df.head())

        # Column selection
        selected_columns = st.multiselect(f"📌 Select Columns - {file.name}", df.columns, default=list(df.columns))
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart (only if numeric columns exist)
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Format conversion
        format_choice = st.radio(f"🔄 Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        # Download button
        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"

            output.seek(0)
            st.download_button("📥 Download File", file_name=new_name, data=output, mime=mime)
            st.success("✅ Processing complete!")
