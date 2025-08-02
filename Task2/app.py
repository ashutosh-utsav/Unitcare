import streamlit as st
import pandas as pd
from processor import summarize_json_with_gemini
from pdf_parser import create_trend_data

st.set_page_config(layout="wide")
st.title("Patient Data Processor")

col1, col2 = st.columns(2)

with col1:
    st.header("Part 1: EMR Visit Summarizer")
    uploaded_json_files = st.file_uploader(
        "Upload one or more EMR JSON files",
        type="json",
        accept_multiple_files=True
    )
    if st.button("Generate Summary"):
        if uploaded_json_files:
            with st.spinner("Generating AI-powered summary..."):
                summary_text = summarize_json_with_gemini(uploaded_json_files)
                st.subheader("EMR Summary")
                st.markdown(summary_text)
        else:
            st.warning("Please upload at least one JSON file.")
    
    st.header("Part 2: Lab Trend Analyzer")
    uploaded_pdf_files = st.file_uploader(
        "Upload one or more Lab Report PDF files",
        type="pdf",
        accept_multiple_files=True
    )
    if st.button("Analyze Trends"):
        if uploaded_pdf_files:
            with st.spinner("Analyzing with AI... this may take a moment."):
                trends_data = create_trend_data(uploaded_pdf_files)
                st.session_state['trends_data'] = trends_data
                if not trends_data:
                    st.error("Could not extract trend data from the provided PDFs.")
        else:
            st.warning("Please upload at least one PDF file.")

with col2:
    st.header("Results")
    if 'trends_data' in st.session_state and st.session_state['trends_data']:
        trends_data = st.session_state['trends_data']
        test_names = list(trends_data.keys())
        
        selected_test = st.selectbox("Select a test to view its trend:", options=test_names)
        
        if selected_test:
            chart_data = trends_data[selected_test]
            df = pd.DataFrame(chart_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date')
            
            st.subheader(f"Trend for {selected_test}")
            st.line_chart(df, x='date', y='value')
            
            st.subheader("Raw Trend Data")
            st.dataframe(df)
    else:
        st.info("Upload and analyze PDFs to see lab trends here.")