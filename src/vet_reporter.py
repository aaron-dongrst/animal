"""
Vet Reporter for ZooGuardian
Generates summary reports of animal health classifications.
"""

import pandas as pd

class VetReporter:
    """
    Generates reports summarizing the classification results.
    """
    
    def __init__(self, output_path: str = "reports/summary_report.xlsx"):
        self.output_path = output_path
    
    def generate_report(self, results: list):
        """
        Generate a summary report from classification results.
        
        Args:
            results: List of classification results.
        """
        # Convert results to a DataFrame
        df = pd.DataFrame(results)
        
        # Save to Excel
        df.to_excel(self.output_path, index=False)
        print(f"Report saved to {self.output_path}")
