import streamlit as st
import re
from collections import Counter
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import io
from typing import Dict, List, Tuple
import time


class LogHeaderAnalyzer:
    """Class to analyze log headers with detailed content tracking"""
    def __init__(self):
        # self.header_pattern = re.compile(r'-+\[(.*?)\]-+')
        self.header_pattern = re.compile(r'-+\[?([^\]]*?)\]?-+')
        self.headers_with_content: Dict[str, List[str]] = {}
        
    def parse_logs(self, text: str) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
        """
        Parse log text and return analysis results
        
        Args:
            text (str): Raw log text to analyze
            
        Returns:
            Tuple containing DataFrame of results and dictionary of header contents
        """
        lines = text.strip().split('\n')
        header_counts = Counter()
        self.headers_with_content.clear()
        
        current_header = None
        current_content = []
        list_content = []
        
        # Process each line
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = self.header_pattern.match(line)
            if match:
                # Save previous header's content
                if current_header and current_content:
                    self.headers_with_content.setdefault(current_header, []).extend(current_content)
                    current_content = []
                
                current_header = match.group(1)
                header_counts[current_header] += 1
                list_content.append({"Header": current_header, "Content": current_content})
            elif current_header:
                current_content.append(line)
                
        
        # Save final header's content
        if current_header and current_content:
            self.headers_with_content.setdefault(current_header, []).extend(current_content)
        
        
        # Create DataFrame for results
        results_data = [
            {"Header": header, "Count": count, "Sample Content": self.headers_with_content.get(header, [''])[0][:50]}
            for header, count in header_counts.items()
        ]
        
        df = pd.DataFrame(results_data)
        
        if not df.empty:
            # Create total row
            total_row = pd.DataFrame([{
                "Header": "TOTAL",
                "Count": df['Count'].sum(),
                "Sample Content": "-"
            }])
            # Use concat instead of append
            df_summury = pd.concat([df, total_row], ignore_index=True)
            df = pd.DataFrame(list_content)
        return df,df_summury, self.headers_with_content

def get_csv_download_link(df: pd.DataFrame) -> str:
    """Generate download link for CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    filename = f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return f'data:file/csv;base64,{b64}'

def generateData() :
    st.spinner()
    file = st.session_state['uploaded_file']
    sheet_name = 'Tickets'
    if file is not None:
        df = pd.read_excel(file, sheet_name=sheet_name)        
        st.success('File Uploaded Successfully', icon="✅")        
        with st.spinner('please Wait for data...'):                    
          time.sleep(2)          
          st.success("Done!")                   
    return None


def main():
    st.set_page_config(
        page_title="Log Analyzer",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Ticket Log Analysis Tool")
    recentFile = st.sidebar.file_uploader("Choose a file",type=["xlsx"],on_change=generateData,key='uploaded_file')
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = LogHeaderAnalyzer()
    
    # Create two columns for input and results
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Log Input")
        log_text = st.text_area(
            "Paste your log text here:",
            height=300,
            key="log_input"
        )
        
        analyze_button = st.button("🔍 Analyze Logs", type="primary")
        
    # Process logs when button is clicked
    if analyze_button and log_text:
        try:
            # Analyze logs
            df,df_summury, content_dict = st.session_state.analyzer.parse_logs(log_text)           
            # Store results in session state
            st.session_state.results_df = df
            st.session_state.results_summmury_df = df_summury
            st.session_state.content_dict = content_dict
            recentFile = st.sidebar.file_uploader("Choose a file",type=["xlsx"],on_change=generateData,key='uploaded_file')
            
            with col2:
                st.subheader("Analysis Results")
                
                # Display results table
                st.dataframe(
                    df_summury,
                    use_container_width=True,
                    hide_index=True
                )
                
                if not df_summury.empty:
                    # Create download button for CSV
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=df.to_csv(index=False),
                        file_name=f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            #dataframe-visualize
            if not df_summury.empty and len(df) > 1:  # Don't include the TOTAL row
                st.subheader("📊 result")
                total_row = pd.DataFrame([{
                    "Header": "TOTAL",
                    "Content": len(df['Header'])                 
                }])
                final_df = pd.concat([df, total_row], ignore_index=True)
                st.dataframe(
                    final_df,
                    use_container_width=True,
                    hide_index=True
                )

            # Display visualization
            if not df_summury.empty and len(df_summury) > 1:  # Don't include the TOTAL row
                st.subheader("📊 Visualization")
                fig = px.bar(
                    df_summury[:-1],  # Exclude the total row
                    x='Header',
                    y='Count',
                    title='Header Distribution',
                    text='Count'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title="Header Type",
                    yaxis_title="Number of Occurrences"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed content viewer
            if content_dict:
                st.subheader("📝 Header Content Details")
                selected_header = st.selectbox(
                    "Select a header to view its content:",
                    options=[h for h in content_dict.keys()]
                )
                
                if selected_header:
                    content = content_dict.get(selected_header, [])
                    if content:
                        st.text_area(
                            f"Content for '{selected_header}':",
                            value="\n".join(content),
                            height=200,
                            disabled=True
                        )
                    else:
                        st.info("No additional content found for this header.")
                    
        except Exception as e:
            st.error(f"Error analyzing logs: {str(e)}")
            st.exception(e)  # This will show the full error traceback in development
            
    elif analyze_button:
        st.warning("Please enter log text to analyze.")

if __name__ == "__main__":
    main()