"""
Data Loading Module

This module handles loading of NYC 311 data, median rent data, and mapping files.
"""

import pandas as pd
import json
from typing import Dict, Tuple, Any


class DataLoader:
    """Handles loading of all required datasets and mapping files."""
    
    def __init__(self, base_path: str = "."):
        """
        Initialize DataLoader with base path.
        
        Args:
            base_path (str): Base path for data files
        """
        self.base_path = base_path
    
    def load_nyc_311_data(self, file_path: str = "data/nyc_311_2024_2025_sample.csv") -> pd.DataFrame:
        """
        Load NYC 311 complaints data.
        
        Args:
            file_path (str): Path to the NYC 311 data file
            
        Returns:
            pd.DataFrame: NYC 311 complaints data with unique_key as index
        """
        full_path = f"{self.base_path}/{file_path}" if self.base_path != "." else file_path
        df = pd.read_csv(full_path, index_col="unique_key")
        print(f"Loaded NYC 311 data: {df.shape}")
        return df
    
    def load_median_rent_data(self, file_path: str = "data/medianAskingRent_All.csv") -> pd.DataFrame:
        """
        Load median rent data.
        
        Args:
            file_path (str): Path to the median rent data file
            
        Returns:
            pd.DataFrame: Median rent data
        """
        full_path = f"{self.base_path}/{file_path}" if self.base_path != "." else file_path
        df = pd.read_csv(full_path)
        print(f"Loaded median rent data: {df.shape}")
        return df
    
    def load_uhf_mapping(self, file_path: str = "nyc_uhf_zipcodes.json") -> Dict[str, Any]:
        """
        Load ZIP code to neighborhood mapping.
        
        Args:
            file_path (str): Path to the UHF mapping file
            
        Returns:
            Dict: ZIP code to neighborhood mapping data
        """
        full_path = f"{self.base_path}/{file_path}" if self.base_path != "." else file_path
        with open(full_path, 'r') as f:
            uhf_data = json.load(f)
        print(f"Loaded UHF mapping data")
        return uhf_data
    
    def load_manual_mapping(self, file_path: str = "manual_map.json") -> Dict[str, str]:
        """
        Load manual mapping for area names to neighborhoods.
        
        Args:
            file_path (str): Path to the manual mapping file
            
        Returns:
            Dict: Manual mapping dictionary
        """
        full_path = f"{self.base_path}/{file_path}" if self.base_path != "." else file_path
        with open(full_path, 'r') as f:
            manual_map = json.load(f)
        print(f"Loaded manual mapping data")
        return manual_map
    
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any], Dict[str, str]]:
        """
        Load all required datasets and mappings.
        
        Returns:
            Tuple containing:
            - NYC 311 DataFrame
            - Median rent DataFrame  
            - UHF mapping dictionary
            - Manual mapping dictionary
        """
        print("Loading all datasets...")
        
        df_nyc_311 = self.load_nyc_311_data()
        df_median_rent = self.load_median_rent_data()
        uhf_data = self.load_uhf_mapping()
        manual_map = self.load_manual_mapping()
        
        print("All datasets loaded successfully!")
        return df_nyc_311, df_median_rent, uhf_data, manual_map
    
    def get_relevant_columns(self) -> list:
        """
        Get list of relevant columns for NYC 311 data analysis.
        
        Returns:
            list: List of relevant column names
        """
        return [
            'created_date', 'closed_date', 'complaint_type',
            'descriptor', 'status', 'resolution_description',
            'resolution_action_updated_date', 'borough',
            'community_board', 'incident_zip', 
            'incident_address', 'street_name', 'city',
            'latitude', 'longitude'
        ]
    
    def display_data_info(self, df_nyc_311: pd.DataFrame, df_median_rent: pd.DataFrame):
        """
        Display basic information about the loaded datasets.
        
        Args:
            df_nyc_311 (pd.DataFrame): NYC 311 data
            df_median_rent (pd.DataFrame): Median rent data
        """
        print("=== NYC 311 Dataset Sample ===")
        print(df_nyc_311.head())
        print("\n=== Median Rent Dataset Sample ===")
        print(df_median_rent.head())