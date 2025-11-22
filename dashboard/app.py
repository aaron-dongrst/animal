"""
Streamlit Dashboard for ZooGuardian
Visualizes animal health classification results.
"""

import streamlit as st
import pandas as pd

def load_results(file_path: str) -> pd.DataFrame:
    """
    Load classification results from an Excel file.
    
    Args:
        file_path: Path to the Excel file.
        
    Returns:
        DataFrame containing the results.
    """
    return pd.read_excel(file_path)

def main():
    st.title("ZooGuardian Dashboard")
    st.write("Visualize animal health classification results.")
    
    # File input
    file_path = st.text_input("Enter the path to the results file:", "reports/summary_report.xlsx")
    
    if st.button("Load Results"):
        try:
            results = load_results(file_path)
            st.write("### Classification Results")
            st.dataframe(results)
            
            # Summary statistics
            st.write("### Summary")
            summary = results['category'].value_counts()
            st.bar_chart(summary)
        except Exception as e:
            st.error(f"Error loading results: {e}")

if __name__ == "__main__":
    main()
