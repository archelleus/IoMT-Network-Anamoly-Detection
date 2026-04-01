"""
IoMT Network Traffic Data Cleaning Script
==========================================
This script cleans training data for anomaly detection in IoMT networks.
Each CSV file is cleaned INDIVIDUALLY and saved separately.

Basic Cleaning Steps (per file):
1. Handle missing values
2. Handle infinite values
3. Remove duplicate rows
4. Save cleaned file

Author: Data Cleaning Pipeline for IoMT Anomaly Detection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')


class IoMTDataCleaner:
    """Class to clean IoMT network traffic data for anomaly detection."""
    
    def __init__(self, data_dir: str, output_dir: str = None):
        """
        Initialize the data cleaner.
        
        Args:
            data_dir: Directory containing the CSV files
            output_dir: Directory to save cleaned data (defaults to data_dir/cleaned)
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir) if output_dir else self.data_dir / "cleaned"
        self.output_dir.mkdir(exist_ok=True)
        
        self.cleaning_reports = {}  # Store report for each file
        
    def _get_numeric_columns(self, df: pd.DataFrame) -> list:
        """Get numeric columns excluding label columns."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        return [c for c in numeric_cols if c not in ['is_attack']]
    
    def _handle_missing_values(self, df: pd.DataFrame, strategy: str = 'median') -> tuple:
        """
        Handle missing values in a dataframe.
        
        Args:
            df: Input dataframe
            strategy: 'mean', 'median', 'mode', 'drop', or 'zero'
        
        Returns:
            Cleaned dataframe and count of missing values handled
        """
        numeric_cols = self._get_numeric_columns(df)
        missing_before = df[numeric_cols].isnull().sum().sum()
        
        if strategy == 'drop':
            df = df.dropna(subset=numeric_cols)
        elif strategy == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'mode':
            for col in numeric_cols:
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col] = df[col].fillna(mode_val[0])
        elif strategy == 'zero':
            df[numeric_cols] = df[numeric_cols].fillna(0)
        
        missing_after = df[numeric_cols].isnull().sum().sum()
        return df, int(missing_before), int(missing_after)
    
    def _handle_infinite_values(self, df: pd.DataFrame, strategy: str = 'clip') -> tuple:
        """
        Handle infinite values in a dataframe.
        
        Args:
            df: Input dataframe
            strategy: 'clip' (replace with max/min), 'nan' (replace with NaN), or 'drop'
        
        Returns:
            Cleaned dataframe and count of infinite values handled
        """
        numeric_cols = self._get_numeric_columns(df)
        inf_before = np.isinf(df[numeric_cols].values).sum()
        
        if strategy == 'clip':
            for col in numeric_cols:
                col_data = df[col].replace([np.inf, -np.inf], np.nan)
                max_val = col_data.max()
                min_val = col_data.min()
                df[col] = df[col].replace(np.inf, max_val)
                df[col] = df[col].replace(-np.inf, min_val)
        elif strategy == 'nan':
            df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan)
        elif strategy == 'drop':
            mask = ~np.isinf(df[numeric_cols].values).any(axis=1)
            df = df[mask]
        
        inf_after = np.isinf(df[numeric_cols].values).sum()
        return df, int(inf_before), int(inf_after)
    
    def _remove_duplicates(self, df: pd.DataFrame) -> tuple:
        """
        Remove duplicate rows from a dataframe.
        
        Returns:
            Cleaned dataframe and count of duplicates removed
        """
        rows_before = len(df)
        df = df.drop_duplicates()
        rows_after = len(df)
        return df, rows_before - rows_after
    
    def clean_file(self, filepath: Path, 
                   missing_strategy: str = 'median',
                   infinite_strategy: str = 'clip') -> dict:
        """
        Clean a single CSV file.
        
        Args:
            filepath: Path to the CSV file
            missing_strategy: Strategy for missing values
            infinite_strategy: Strategy for infinite values
        
        Returns:
            Cleaning report dictionary
        """
        filename = filepath.name
        print(f"\n{'='*60}")
        print(f"📁 Cleaning: {filename}")
        print(f"{'='*60}")
        
        # Load the file
        df = pd.read_csv(filepath)
        initial_rows = len(df)
        initial_cols = len(df.columns)
        print(f"  📊 Loaded: {initial_rows:,} rows, {initial_cols} columns")
        
        # Check initial quality
        numeric_cols = self._get_numeric_columns(df)
        initial_missing = df[numeric_cols].isnull().sum().sum()
        initial_inf = np.isinf(df[numeric_cols].values).sum()
        initial_duplicates = df.duplicated().sum()
        
        print(f"  📋 Initial issues:")
        print(f"     - Missing values: {initial_missing:,}")
        print(f"     - Infinite values: {initial_inf:,}")
        print(f"     - Duplicate rows: {initial_duplicates:,}")
        
        # Step 1: Handle missing values
        df, missing_before, missing_after = self._handle_missing_values(df, missing_strategy)
        print(f"  ✓ Missing values: {missing_before:,} → {missing_after:,} ({missing_strategy})")
        
        # Step 2: Handle infinite values
        df, inf_before, inf_after = self._handle_infinite_values(df, infinite_strategy)
        print(f"  ✓ Infinite values: {inf_before:,} → {inf_after:,} ({infinite_strategy})")
        
        # Step 3: Remove duplicates
        df, duplicates_removed = self._remove_duplicates(df)
        print(f"  ✓ Duplicates removed: {duplicates_removed:,}")
        
        # Save cleaned file (keep original name)
        output_filename = filepath.name
        output_path = self.output_dir / output_filename
        df.to_csv(output_path, index=False)
        
        final_rows = len(df)
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        print(f"  💾 Saved: {output_path.name}")
        print(f"     - Final rows: {final_rows:,} ({initial_rows - final_rows:,} removed)")
        print(f"     - Size: {file_size_mb:.2f} MB")
        
        # Create report
        report = {
            'original_file': filename,
            'cleaned_file': output_filename,
            'initial_rows': initial_rows,
            'final_rows': final_rows,
            'rows_removed': initial_rows - final_rows,
            'initial_columns': initial_cols,
            'missing_values': {'before': missing_before, 'after': missing_after, 'strategy': missing_strategy},
            'infinite_values': {'before': inf_before, 'after': inf_after, 'strategy': infinite_strategy},
            'duplicates_removed': duplicates_removed,
            'output_size_mb': round(file_size_mb, 2)
        }
        
        return report
    
    def clean_all_files(self, 
                        missing_strategy: str = 'median',
                        infinite_strategy: str = 'clip'):
        """
        Clean all CSV files in the data directory individually.
        
        Args:
            missing_strategy: Strategy for missing values ('mean', 'median', 'mode', 'drop', 'zero')
            infinite_strategy: Strategy for infinite values ('clip', 'nan', 'drop')
        """
        print("\n" + "=" * 60)
        print("🚀 IoMT DATA CLEANING - INDIVIDUAL FILE PROCESSING")
        print("=" * 60)
        print(f"📂 Source: {self.data_dir}")
        print(f"📂 Output: {self.output_dir}")
        print(f"🔧 Missing values strategy: {missing_strategy}")
        print(f"🔧 Infinite values strategy: {infinite_strategy}")
        
        csv_files = list(self.data_dir.glob("*.csv"))
        print(f"\n📋 Found {len(csv_files)} CSV files to clean")
        
        total_initial_rows = 0
        total_final_rows = 0
        total_missing = 0
        total_infinite = 0
        total_duplicates = 0
        
        for csv_file in csv_files:
            report = self.clean_file(csv_file, missing_strategy, infinite_strategy)
            self.cleaning_reports[report['original_file']] = report
            
            total_initial_rows += report['initial_rows']
            total_final_rows += report['final_rows']
            total_missing += report['missing_values']['before']
            total_infinite += report['infinite_values']['before']
            total_duplicates += report['duplicates_removed']
        
        # Save overall report
        report_path = self.output_dir / 'cleaning_report.json'
        overall_report = {
            'files_processed': len(csv_files),
            'total_initial_rows': total_initial_rows,
            'total_final_rows': total_final_rows,
            'total_rows_removed': total_initial_rows - total_final_rows,
            'total_missing_values_handled': total_missing,
            'total_infinite_values_handled': total_infinite,
            'total_duplicates_removed': total_duplicates,
            'missing_strategy': missing_strategy,
            'infinite_strategy': infinite_strategy,
            'file_reports': self.cleaning_reports
        }
        
        with open(report_path, 'w') as f:
            json.dump(overall_report, f, indent=2)
        
        # Final summary
        print("\n" + "=" * 60)
        print("✅ CLEANING COMPLETE - SUMMARY")
        print("=" * 60)
        print(f"  � Files processed: {len(csv_files)}")
        print(f"  📊 Total initial rows: {total_initial_rows:,}")
        print(f"  📊 Total final rows: {total_final_rows:,}")
        print(f"  📊 Total rows removed: {total_initial_rows - total_final_rows:,}")
        print(f"  � Missing values handled: {total_missing:,}")
        print(f"  � Infinite values handled: {total_infinite:,}")
        print(f"  � Duplicates removed: {total_duplicates:,}")
        print(f"  📄 Report saved: {report_path}")
        print(f"  � Output directory: {self.output_dir}")
        
        return self.cleaning_reports


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    # Configuration
    DATA_DIR = "/home/bhavya-jain/Code/PBL/test"
    OUTPUT_DIR = "/home/bhavya-jain/Code/PBL/data/test/cleaned"
    
    # Create cleaner instance
    cleaner = IoMTDataCleaner(data_dir=DATA_DIR, output_dir=OUTPUT_DIR)
    
    # Clean all files individually
    cleaner.clean_all_files(
        missing_strategy='median',   # Options: median, mean, mode, drop, zero
        infinite_strategy='clip'     # Options: clip, nan, drop
    )
    
    print("\n✅ Data cleaning complete! Check the 'cleaned' directory for output files.")

