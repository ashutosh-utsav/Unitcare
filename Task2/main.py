import streamlit as st
import pandas as pd
from processor import summarize_json_with_gemini
from pdf_parser import create_trend_data

st.set_page_config(layout="wide")
st.title("Patient Data Processor")

col1, col2 = st.columns(2)

with col1:
    st.header("Inputs")

    st.subheader("Part 1: EMR Visit Summarizer")
    with st.form("json_form"):
        uploaded_json_files = st.file_uploader(
            "Upload one or more EMR JSON files",
            type="json",
            accept_multiple_files=True
        )
        json_submitted = st.form_submit_button("Generate Summary")
    
    if json_submitted and uploaded_json_files:
        with st.spinner("Generating AI-powered summary..."):
            summary_text = summarize_json_with_gemini(uploaded_json_files)
            st.session_state['summary_text'] = summary_text
            st.success("Summary generated!")

    st.subheader("Part 2: Lab Trend Analyzer")
    with st.form("pdf_form"):
        uploaded_pdf_files = st.file_uploader(
            "Upload one or more Lab Report PDF files",
            type="pdf",
            accept_multiple_files=True
        )
        pdf_submitted = st.form_submit_button("Analyze Trends")

    if pdf_submitted and uploaded_pdf_files:
        with st.spinner("Analyzing with AI... this may take a moment."):
            trends_data = create_trend_data(uploaded_pdf_files)
            st.session_state['trends_data'] = trends_data
            if not trends_data:
                st.error("Could not extract trend data from the provided PDFs.")
            else:
                st.success("Trend analysis complete!")

with col2:
    st.header("Results")

    if 'summary_text' in st.session_state:
        st.subheader("EMR Summary")
        st.markdown(st.session_state['summary_text'])
    else:
        st.info("Upload JSON files and click 'Generate Summary' to see the result here.")

    st.markdown("---")

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