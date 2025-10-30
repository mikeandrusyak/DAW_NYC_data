"""
Utilities Module

This module contains utility functions for data quality checking and analysis.
"""

import pandas as pd
from typing import Dict, List, Any


class DataQualityChecker:
    """Utility class for data quality checking and analysis."""
    
    def __init__(self):
        """Initialize DataQualityChecker."""
        pass
    
    def check_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Check data types of all columns in DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: Summary of data types and non-null counts
        """
        info_dict = {
            'Column': df.columns,
            'Data_Type': df.dtypes.values,
            'Non_Null_Count': df.count().values,
            'Null_Count': df.isnull().sum().values,
            'Null_Percentage': (df.isnull().sum() / len(df) * 100).round(2).values
        }
        
        return pd.DataFrame(info_dict)
    
    def get_unique_values_summary(self, df: pd.DataFrame, 
                                categorical_columns: List[str] = None) -> Dict[str, int]:
        """
        Get summary of unique values for categorical columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            categorical_columns (List[str]): List of categorical columns to analyze
            
        Returns:
            Dict[str, int]: Dictionary with column names and unique value counts
        """
        if categorical_columns is None:
            # Auto-detect categorical columns
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        unique_summary = {}
        for col in categorical_columns:
            if col in df.columns:
                unique_summary[col] = df[col].nunique()
        
        return unique_summary
    
    def check_date_ranges(self, df: pd.DataFrame, date_columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Check date ranges for date columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_columns (List[str]): List of date columns to check
            
        Returns:
            Dict: Date range information for each column
        """
        date_info = {}
        
        for col in date_columns:
            if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
                date_info[col] = {
                    'min_date': df[col].min(),
                    'max_date': df[col].max(),
                    'date_range_days': (df[col].max() - df[col].min()).days,
                    'null_count': df[col].isnull().sum()
                }
        
        return date_info
    
    def detect_outliers_iqr(self, df: pd.DataFrame, column: str, 
                          multiplier: float = 1.5) -> pd.DataFrame:
        """
        Detect outliers using IQR method.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            column (str): Column to check for outliers
            multiplier (float): IQR multiplier for outlier detection
            
        Returns:
            pd.DataFrame: Outlier analysis results
        """
        if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
            print(f"Column {column} not found or not numeric")
            return pd.DataFrame()
        
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        analysis = {
            'total_records': len(df),
            'outliers_count': len(outliers),
            'outliers_percentage': (len(outliers) / len(df) * 100).round(2),
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
        
        return pd.DataFrame([analysis])
    
    def generate_data_profile(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
        """
        Generate comprehensive data profile.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            dataset_name (str): Name of the dataset
            
        Returns:
            Dict: Comprehensive data profile
        """
        profile = {
            'dataset_name': dataset_name,
            'shape': df.shape,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'data_types': self.check_data_types(df),
            'unique_values': self.get_unique_values_summary(df),
            'missing_data_summary': {
                'total_missing': df.isnull().sum().sum(),
                'columns_with_missing': df.columns[df.isnull().any()].tolist(),
                'missing_percentage_by_column': (df.isnull().sum() / len(df) * 100).round(2).to_dict()
            }
        }
        
        # Add date analysis if date columns exist
        date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        if date_columns:
            profile['date_analysis'] = self.check_date_ranges(df, date_columns)
        
        # Add numeric analysis if numeric columns exist
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if numeric_columns:
            profile['numeric_summary'] = df[numeric_columns].describe().to_dict()
        
        return profile
    
    def print_data_profile(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> None:
        """
        Print formatted data profile.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            dataset_name (str): Name of the dataset
        """
        profile = self.generate_data_profile(df, dataset_name)
        
        print(f"=== Data Profile for {profile['dataset_name']} ===")
        print(f"Shape: {profile['shape']}")
        print(f"Memory Usage: {profile['memory_usage_mb']:.2f} MB")
        
        print(f"\n=== Missing Data ===")
        print(f"Total missing values: {profile['missing_data_summary']['total_missing']}")
        print(f"Columns with missing data: {len(profile['missing_data_summary']['columns_with_missing'])}")
        
        if profile['missing_data_summary']['columns_with_missing']:
            print("Missing data by column:")
            for col, pct in profile['missing_data_summary']['missing_percentage_by_column'].items():
                if pct > 0:
                    print(f"  {col}: {pct}%")
        
        print(f"\n=== Unique Values ===")
        for col, count in profile['unique_values'].items():
            print(f"{col}: {count} unique values")
        
        if 'date_analysis' in profile:
            print(f"\n=== Date Analysis ===")
            for col, info in profile['date_analysis'].items():
                print(f"{col}: {info['min_date']} to {info['max_date']} ({info['date_range_days']} days)")
    
    def compare_datasets(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                        name1: str = "Dataset 1", name2: str = "Dataset 2") -> Dict[str, Any]:
        """
        Compare two datasets.
        
        Args:
            df1 (pd.DataFrame): First dataset
            df2 (pd.DataFrame): Second dataset
            name1 (str): Name of first dataset
            name2 (str): Name of second dataset
            
        Returns:
            Dict: Comparison results
        """
        comparison = {
            'dataset_names': (name1, name2),
            'shapes': (df1.shape, df2.shape),
            'common_columns': list(set(df1.columns) & set(df2.columns)),
            'unique_to_first': list(set(df1.columns) - set(df2.columns)),
            'unique_to_second': list(set(df2.columns) - set(df1.columns)),
            'data_type_differences': {}
        }
        
        # Check data type differences for common columns
        for col in comparison['common_columns']:
            if df1[col].dtype != df2[col].dtype:
                comparison['data_type_differences'][col] = {
                    name1: str(df1[col].dtype),
                    name2: str(df2[col].dtype)
                }
        
        return comparison
    
    def validate_data_integrity(self, df: pd.DataFrame) -> Dict[str, bool]:
        """
        Validate data integrity checks.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            Dict[str, bool]: Validation results
        """
        validations = {
            'no_duplicates': not df.duplicated().any(),
            'no_empty_dataframe': len(df) > 0,
            'consistent_data_types': len(df.dtypes.value_counts()) > 0,
            'no_infinite_values': not df.select_dtypes(include=['float64', 'int64']).isin([float('inf'), float('-inf')]).any().any()
        }
        
        return validations