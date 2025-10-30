"""
NYC Data Wrangling Pipeline - Simplified Version

Simplified pipeline for step-by-step processing of NYC data.
Contains only the 4 main steps without additional convenience methods.
"""

import pandas as pd
from typing import Dict, Any, Tuple

from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .data_transformer import DataTransformer
from .data_integrator import DataIntegrator


class NYCDataPipeline:
    """Simplified pipeline for step-by-step processing of NYC data."""
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the pipeline.

        Args:
            base_path (str): Base path for data files
        """
        self.base_path = base_path
        self.loader = DataLoader(base_path)
        self.cleaner = DataCleaner()
        self.transformer = DataTransformer()
        self.integrator = DataIntegrator()
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any], Dict[str, str]]:
        """
        Step 1: Load all required datasets.

        Returns:
            Tuple: (NYC 311 DataFrame, median rent DataFrame, UHF mapping dict, manual mapping dict)
        """
        print("=" * 50)
        print("STEP 1: LOADING DATA")
        print("=" * 50)

        # Load all datasets
        df_nyc_311, df_median_rent, uhf_data, manual_map = self.loader.load_all_data()

        # Display basic information about loaded datasets
        self.loader.display_data_info(df_nyc_311, df_median_rent)

        return df_nyc_311, df_median_rent, uhf_data, manual_map
    
    def clean_data(self, df_nyc_311: pd.DataFrame, 
                   df_median_rent: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Step 2: Clean both datasets.

        Args:
            df_nyc_311: Raw NYC 311 DataFrame
            df_median_rent: Raw median rent DataFrame

        Returns:
            Tuple: (cleaned NYC 311 DataFrame, cleaned median rent DataFrame)
        """
        print("\n" + "=" * 50)
        print("STEP 2: CLEANING DATA")
        print("=" * 50)

        # Get relevant columns for NYC 311
        relevant_columns = self.loader.get_relevant_columns()

        # Clean NYC 311 data
        df_nyc_311_cleaned = self.cleaner.clean_nyc_311_data(df_nyc_311, relevant_columns)

        # Clean median rent data
        df_median_rent_cleaned = self.cleaner.clean_rent_data(df_median_rent)

        return df_nyc_311_cleaned, df_median_rent_cleaned
    
    def transform_data(self, df_nyc_311_cleaned: pd.DataFrame,
                      df_median_rent_cleaned: pd.DataFrame,
                      uhf_data: Dict[str, Any],
                      manual_map: Dict[str, str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Step 3: Transform both datasets.

        Args:
            df_nyc_311_cleaned: Cleaned NYC 311 DataFrame
            df_median_rent_cleaned: Cleaned median rent DataFrame
            uhf_data: UHF mapping dictionary
            manual_map: Manual neighborhood mapping dictionary

        Returns:
            Tuple: (transformed NYC 311 DataFrame, transformed median rent DataFrame)
        """
        print("\n" + "=" * 50)
        print("STEP 3: TRANSFORMING DATA")
        print("=" * 50)

        # Transform NYC 311 data
        df_nyc_311_transformed = self.transformer.transform_nyc_311_data(
            df_nyc_311_cleaned, uhf_data
        )

        # Transform median rent data
        df_median_rent_transformed = self.transformer.transform_rent_data(
            df_median_rent_cleaned, manual_map
        )

        return df_nyc_311_transformed, df_median_rent_transformed
    
    def aggregate_and_integrate(self, df_nyc_311_transformed: pd.DataFrame,
                               df_median_rent_transformed: pd.DataFrame) -> pd.DataFrame:
        """
        Step 4: Aggregate and integrate datasets.

        Args:
            df_nyc_311_transformed: Transformed NYC 311 DataFrame
            df_median_rent_transformed: Transformed median rent DataFrame

        Returns:
            pd.DataFrame: Final integrated dataset
        """
        print("\n" + "=" * 50)
        print("STEP 4: AGGREGATION AND INTEGRATION")
        print("=" * 50)

        # Aggregate complaints by neighborhood
        complaints_aggregated = self.transformer.aggregate_complaints_by_neighborhood(
            df_nyc_311_transformed
        )

        # Aggregate rent data by neighborhood
        rent_aggregated = self.transformer.aggregate_rent_by_neighborhood(
            df_median_rent_transformed
        )

        # Reshape rent data from wide to long format
        rent_reshaped = self.transformer.reshape_rent_data(rent_aggregated)

        # Integrate datasets
        final_dataset = self.integrator.create_final_dataset(
            complaints_aggregated, rent_reshaped
        )

        return final_dataset