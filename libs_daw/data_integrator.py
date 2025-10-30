"""
Data Integration Module

This module handles merging and integration of different datasets.
"""

import pandas as pd
from typing import List


class DataIntegrator:
    """Handles data integration and merging operations."""
    
    def __init__(self):
        """Initialize DataIntegrator."""
        pass
    
    def merge_complaints_and_rent(self, complaints_df: pd.DataFrame, 
                                 rent_df: pd.DataFrame,
                                 merge_columns: List[str] = None,
                                 how: str = 'left') -> pd.DataFrame:
        """
        Merge complaints and rent data.
        
        Args:
            complaints_df (pd.DataFrame): Aggregated complaints data
            rent_df (pd.DataFrame): Reshaped rent data
            merge_columns (List[str]): Columns to merge on
            how (str): Type of merge to perform
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        if merge_columns is None:
            merge_columns = ['neighborhood', 'year', 'month']
        
        # Select relevant columns from rent data for merging
        rent_columns_for_merge = merge_columns + ['median_rent']
        
        df_merged = pd.merge(
            complaints_df, 
            rent_df[rent_columns_for_merge], 
            on=merge_columns, 
            how=how
        )

        print(f"Final merged dataset shape: {df_merged.shape}")
        print(f"Records with rent data: {df_merged['median_rent'].notna().sum()}")
        print(f"Records without rent data: {df_merged['median_rent'].isna().sum()}")
        
        return df_merged
    
    def create_final_dataset(self, complaints_df: pd.DataFrame, 
                           rent_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create final integrated dataset from complaints and rent data.
        
        Args:
            complaints_df (pd.DataFrame): Aggregated complaints data
            rent_df (pd.DataFrame): Reshaped rent data
            
        Returns:
            pd.DataFrame: Final integrated dataset
        """
        print("Creating final integrated dataset...")
        
        # Merge the datasets
        df_final = self.merge_complaints_and_rent(complaints_df, rent_df)
        
        print("Final dataset integration completed!")
        return df_final
    
    def export_dataset(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Export dataset to CSV file.
        
        Args:
            df (pd.DataFrame): DataFrame to export
            output_path (str): Path for output file
        """
        df.to_csv(output_path, index=False)
        print(f"Dataset exported to: {output_path}")
        print(f"Dataset shape: {df.shape}")
    
    def get_dataset_summary(self, df: pd.DataFrame) -> dict:
        """
        Get summary statistics for the final dataset.
        
        Args:
            df (pd.DataFrame): Final dataset
            
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_records': len(df),
            'date_range': f"{df['year'].min()}-{df['year'].max()}",
            'unique_neighborhoods': df['neighborhood'].nunique(),
            'unique_complaint_types': df['complaint_type'].nunique(),
            'data_completeness': (df.notna().sum() / len(df) * 100).round(2).to_dict()
        }
        
        return summary
    
    def print_dataset_summary(self, df: pd.DataFrame) -> None:
        """
        Print comprehensive dataset summary.
        
        Args:
            df (pd.DataFrame): Final dataset
        """
        summary = self.get_dataset_summary(df)
        
        print("=== Final Dataset Summary ===")
        print(f"Total records: {summary['total_records']:,}")
        print(f"Date range: {summary['date_range']}")
        print(f"Unique neighborhoods: {summary['unique_neighborhoods']}")
        print(f"Unique complaint types: {summary['unique_complaint_types']}")

        print("\n=== Data Completeness ===")
        for column, completeness in summary['data_completeness'].items():
            print(f"{column}: {completeness}%")

        print("\n=== Top 10 Neighborhoods by Complaint Volume ===")
        top_neighborhoods = df.groupby('neighborhood')['complaint_count'].sum().sort_values(ascending=False).head(10)
        for neighborhood, count in top_neighborhoods.items():
            print(f"{neighborhood}: {count:,}")
    
    def validate_merged_data(self, df: pd.DataFrame) -> dict:
        """
        Validate the quality of merged data.
        
        Args:
            df (pd.DataFrame): Merged dataset
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'has_duplicates': df.duplicated().any(),
            'missing_neighborhoods': df['neighborhood'].isna().sum(),
            'missing_rent_data': df['median_rent'].isna().sum(),
            'invalid_years': (df['year'] < 2024).sum() + (df['year'] > 2025).sum(),
            'invalid_months': (df['month'] < 1).sum() + (df['month'] > 12).sum(),
            'negative_complaints': (df['complaint_count'] < 0).sum(),
            'negative_resolution_time': (df['median_resolution_time_hours'] < 0).sum()
        }
        
        return validation_results
    
    def print_validation_results(self, df: pd.DataFrame) -> None:
        """
        Print data validation results.
        
        Args:
            df (pd.DataFrame): Dataset to validate
        """
        results = self.validate_merged_data(df)
        
        print("=== Data Validation Results ===")
        for check, value in results.items():
            status = "✓ PASS" if value == 0 else f"✗ FAIL ({value})"
            print(f"{check.replace('_', ' ').title()}: {status}")
    
    def get_sample_data(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Get sample of merged data for inspection.
        
        Args:
            df (pd.DataFrame): Dataset
            n (int): Number of samples to return
            
        Returns:
            pd.DataFrame: Sample data
        """
        return df.head(n)