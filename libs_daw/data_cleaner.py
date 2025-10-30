"""
Data Cleaning Module

This module handles cleaning and preprocessing of NYC 311 and median rent data.
"""

import pandas as pd
from typing import List, Tuple


class DataCleaner:
    """Handles data cleaning operations for NYC datasets."""
    
    def __init__(self):
        """Initialize DataCleaner."""
        pass
    
    def select_relevant_columns(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Select relevant columns from DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): List of column names to select
            
        Returns:
            pd.DataFrame: DataFrame with selected columns
        """
        df_selected = df[columns].copy()
        print(f"Selected {len(columns)} columns from dataset")
        return df_selected
    
    def select_rent_date_columns(self, df: pd.DataFrame, years: List[str] = None) -> pd.DataFrame:
        """
        Select relevant date columns from rent data.
        
        Args:
            df (pd.DataFrame): Median rent DataFrame
            years (List[str]): Years to include (default: ['2024', '2025'])
            
        Returns:
            pd.DataFrame: DataFrame with selected columns
        """
        if years is None:
            years = ['2024', '2025']
        
        date_columns = [col for col in df.columns 
                       if any(col.startswith(year) for year in years)]
        
        # Include first 3 info columns plus date columns
        selected_columns = df.columns[:3].to_list() + date_columns
        df_selected = df[selected_columns].copy()
        
        print(f"Selected {len(date_columns)} date columns plus 3 info columns from rent data")
        return df_selected
    
    def analyze_missing_values(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> pd.DataFrame:
        """
        Analyze missing values in DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            dataset_name (str): Name of dataset for reporting
            
        Returns:
            pd.DataFrame: Missing values analysis
        """
        missing_values = df.isna().sum().sort_values(ascending=False)
        missing_percentage = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)

        missing_data = pd.DataFrame({
            'Missing_Count': missing_values,
            'Missing_Percentage': missing_percentage
        })

        # Only show columns with missing values
        missing_data = missing_data[missing_data['Missing_Count'] > 0]

        print(f"Total number of rows in {dataset_name}: {len(df)}")
        print(f"\nMissing values analysis for {dataset_name}:")
        
        return missing_data.round(2)
    
    def remove_duplicates(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            dataset_name (str): Name of dataset for reporting
            
        Returns:
            pd.DataFrame: DataFrame with duplicates removed
        """
        original_shape = df.shape
        duplicates_count = df.duplicated().sum()
        
        print(f"Duplicate rows in {dataset_name}: {duplicates_count}")
        
        if duplicates_count > 0:
            df_cleaned = df.drop_duplicates()
            print(f"Removed {original_shape[0] - df_cleaned.shape[0]} duplicate rows from {dataset_name}")
            print(f"New shape: {df_cleaned.shape}")
            return df_cleaned
        
        return df
    
    def clean_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """
        Clean and convert date columns to datetime format.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_columns (List[str]): List of date column names
            
        Returns:
            pd.DataFrame: DataFrame with cleaned dates
        """
        df_cleaned = df.copy()
        
        # Convert date columns to datetime
        for col in date_columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
        
        # Remove invalid date records (created_date > closed_date)
        if 'created_date' in df_cleaned.columns and 'closed_date' in df_cleaned.columns:
            invalid_dates = df_cleaned[df_cleaned['created_date'] > df_cleaned['closed_date']]
            print(f"Number of rows with created_date > closed_date (will be removed): {invalid_dates.shape[0]}")

            df_cleaned = df_cleaned[
                (df_cleaned['created_date'] <= df_cleaned['closed_date']) | 
                (df_cleaned['closed_date'].isna())
            ]
            
            print(f"Final data shape after date cleaning: {df_cleaned.shape}")
        
        return df_cleaned
    
    def clean_geographic_data(self, df: pd.DataFrame, city_column: str = 'city') -> pd.DataFrame:
        """
        Clean geographic data (city names).
        
        Args:
            df (pd.DataFrame): Input DataFrame
            city_column (str): Name of city column
            
        Returns:
            pd.DataFrame: DataFrame with cleaned geographic data
        """
        df_cleaned = df.copy()
        
        if city_column in df_cleaned.columns:
            # Standardize city names: trim whitespace and convert to uppercase
            df_cleaned[city_column] = df_cleaned[city_column].str.strip().str.upper()

            # Replace known outside NYC locations with 'OUTSIDE NYC'
            outside_nyc_locations = ['FLORAL PARK', 'NEW HYDE PARK', 'BREEZY POINT']
            df_cleaned[city_column] = df_cleaned[city_column].replace(outside_nyc_locations, 'OUTSIDE NYC')

            print("City names standardized")
            print(f"Unique cities after cleaning: {df_cleaned[city_column].nunique()}")
        
        return df_cleaned
    
    def clean_nyc_311_data(self, df: pd.DataFrame, relevant_columns: List[str]) -> pd.DataFrame:
        """
        Complete cleaning pipeline for NYC 311 data.
        
        Args:
            df (pd.DataFrame): Raw NYC 311 DataFrame
            relevant_columns (List[str]): List of relevant columns to select
            
        Returns:
            pd.DataFrame: Cleaned NYC 311 DataFrame
        """
        print("Starting NYC 311 data cleaning pipeline...")
        
        # Select relevant columns
        df_cleaned = self.select_relevant_columns(df, relevant_columns)
        
        # Analyze missing values
        self.analyze_missing_values(df_cleaned, "NYC 311")
        
        # Remove duplicates
        df_cleaned = self.remove_duplicates(df_cleaned, "NYC 311")
        
        # Clean dates
        date_columns = ['created_date', 'closed_date', 'resolution_action_updated_date']
        df_cleaned = self.clean_dates(df_cleaned, date_columns)
        
        # Clean geographic data
        df_cleaned = self.clean_geographic_data(df_cleaned, 'city')
        
        print("NYC 311 data cleaning completed!")
        return df_cleaned
    
    def clean_rent_data(self, df: pd.DataFrame, years: List[str] = None) -> pd.DataFrame:
        """
        Complete cleaning pipeline for median rent data.
        
        Args:
            df (pd.DataFrame): Raw median rent DataFrame
            years (List[str]): Years to include in analysis
            
        Returns:
            pd.DataFrame: Cleaned median rent DataFrame
        """
        print("Starting median rent data cleaning pipeline...")
        
        # Select relevant columns
        df_cleaned = self.select_rent_date_columns(df, years)
        
        # Analyze missing values
        self.analyze_missing_values(df_cleaned, "Median Rent")
        
        # Remove duplicates
        df_cleaned = self.remove_duplicates(df_cleaned, "Median Rent")
        
        print("Median rent data cleaning completed!")
        return df_cleaned