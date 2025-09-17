# -*- coding: utf-8 -*-
"""
Liu et al. (2022) data access functions.

This module provides functions to load magnetic field data from Liu et al. (2022),
which contains a complete compilation of all DCF (Davis-Chandrasekhar-Fermi) estimations.
"""

import pandas as pd
from io import StringIO
from maguniverse.utils import get_default_data_paths, get_ascii
from maguniverse.data.processed.sources import processed_data_tables


def get_liu2022(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """Load the Liu et al. (2022) DCF estimations data into a DataFrame.

    This function reads and processes the DCF sample data table from Liu et al. (2022),
    which contains magnetic field strength estimations using the Davis-Chandrasekhar-Fermi method.

    Parameters
    ----------
    file_path : str, optional
        Local filesystem path to the ASCII data. If None, defaults are used.
    file_url : str, optional
        URL to download the ASCII data. If None, defaults are used.
    save_path : str, optional
        If provided, the resulting DataFrame is written to this CSV path.
    save_src_data_path : str, optional
        If provided, the raw ASCII data is saved to this path.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the following columns:
        - Name : Identifier (string)
        - Inst : Instrument (string)
        - Method : Method used (string)
        - r : Radius in parsecs (float, optional)
        - M : Mass in solar masses (float, optional)
        - nH2 : H2 density in cm^-3 (float, optional)
        - NH2 : H2 column density in cm^-2 (float, optional)
        - deltavlos : Line-of-sight turbulent velocity dispersion in km/s (float, optional)
        - deltaphi : Measured angular dispersion in degrees (float, optional)
        - Ratio : Turbulent-to-ordered magnetic field strength ratio (float, optional)
        - Nadf : Number of turbulent fluid elements along line of sight (float, optional)
        - deltaadf : Turbulent correlation length in mpc (float, optional)
        - Bu_ref : Referenced plane-of-sky uniform magnetic field strength in μG (int, optional)
        - Bu_est : Re-estimated plane-of-sky uniform magnetic field strength in μG (int, optional)
        - Btot_est : Estimated plane-of-sky total magnetic field strength in μG (int, optional)
        - alphaB : Magnetic virial parameter (float, optional)
        - BibCode : Reference bibcode (string)

    Raises
    ------
    ValueError
        If both file_path and file_url are provided but point to different sources.
    TypeError
        If save_path or save_src_data_path are not strings when provided.
    """
    # Input validation
    if save_path is not None and not isinstance(save_path, str):
        raise TypeError("save_path must be a string")
    if save_src_data_path is not None and not isinstance(save_src_data_path, str):
        raise TypeError("save_src_data_path must be a string")

    # Get default paths if none provided
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            processed_data_tables['Liu2022']['data_link']['t1_data_table_local'],
            processed_data_tables['Liu2022']['data_link']['t1_data_table_ascii']
        )
    
    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Parse the data
    lines = raw.split('\n')
    
    # Find the data section (starts after the header lines)
    data_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('SMM-NW') or line.strip().startswith('CB26'):
            data_start = i
            break
    
    if data_start is None:
        raise ValueError("Could not find data section in the file")
    
    # Extract data lines
    data_lines = lines[data_start:]
    
    # Define column names based on the file format description
    column_names = [
        'Name', 'Inst', 'Method', 'r', 'M', 'nH2', 'NH2', 'deltavlos', 
        'deltaphi', 'Ratio', 'Nadf', 'deltaadf', 'Bu_ref', 'Bu_est', 
        'Btot_est', 'alphaB', 'BibCode'
    ]
    
    # Parse each data line using fixed-width format
    parsed_data = []
    for line in data_lines:
        line = line.rstrip('\n')  # Remove newline but keep spaces
        if not line.strip():  # Skip empty lines
            continue
            
        # Extract data using fixed-width positions based on the format description
        # Bytes Format Units   Label      Explanations
        # 1- 17 A17    ---     Name       Identifier
        # 19- 24 A6     ---     Inst       Instrument 
        # 26- 30 A5     ---     Method     Method 
        # 32- 37 F6.3   pc      r          ? Radius
        # 39- 47 F9.2   solMass M          ? Mass
        # 49- 53 E5.1   cm-3    nH2        ? H_2_ density
        # 55- 60 E6.1   cm-2    NH2        ? H2 column density
        # 62- 65 F4.2   km/s    deltavlos  ? Line-of-sight turbulent velocity dispersion
        # 67- 70 F4.1   deg     deltaphi   ? Measured angular dispersion
        # 72- 74 F3.1   ---     Ratio      ? Turbulent-to-ordered magnetic field strength ratio
        # 76- 79 F4.1   ---     Nadf       ? Number of turbulent fluid elements along line of sight
        # 81- 85 F5.1   mpc     deltaadf   ? Turbulent correlation length
        # 87- 91 I5     ugauss  Bu,ref     Referenced plane-of-sky uniform magnetic field strength
        # 93- 97 I5     ugauss  Bu,est     ? Re-estimated plane-of-sky uniform magnetic field strength
        # 99-103 I5     ugauss  Btot,est   Estimated plane-of-sky total magnetic field strength
        # 105-109 F5.2   ---     alphaB     ? Magnetic virial parameter
        # 111-129 A19    ---     BibCode    Reference bibcode
        
        # Create a dictionary for this row
        row_data = {}
        
        # Extract fields using fixed-width positions (1-indexed, so subtract 1 for 0-indexed)
        def extract_field(line, start, end, field_type=str):
            if len(line) < end:
                return None
            field = line[start-1:end].strip()
            if not field or field == '---':
                return None
            try:
                if field_type == int:
                    return int(field)
                elif field_type == float:
                    return float(field)
                else:
                    return field
            except (ValueError, TypeError):
                return None
        
        row_data['Name'] = extract_field(line, 1, 17)
        row_data['Inst'] = extract_field(line, 19, 24)
        row_data['Method'] = extract_field(line, 26, 30)
        row_data['r'] = extract_field(line, 32, 37, float)
        row_data['M'] = extract_field(line, 39, 47, float)
        row_data['nH2'] = extract_field(line, 49, 53, float)
        row_data['NH2'] = extract_field(line, 55, 60, float)
        row_data['deltavlos'] = extract_field(line, 62, 65, float)
        row_data['deltaphi'] = extract_field(line, 67, 70, float)
        row_data['Ratio'] = extract_field(line, 72, 74, float)
        row_data['Nadf'] = extract_field(line, 76, 79, float)
        row_data['deltaadf'] = extract_field(line, 81, 85, float)
        row_data['Bu_ref'] = extract_field(line, 87, 91, int)
        row_data['Bu_est'] = extract_field(line, 93, 97, int)
        row_data['Btot_est'] = extract_field(line, 99, 103, int)
        row_data['alphaB'] = extract_field(line, 105, 109, float)
        row_data['BibCode'] = extract_field(line, 111, 129)
        
        # Only add rows that have at least a name
        if row_data['Name']:
            parsed_data.append(row_data)
    
    # Create DataFrame
    df = pd.DataFrame(parsed_data)
    
    # Convert numeric columns to appropriate types
    numeric_columns = ['r', 'M', 'nH2', 'NH2', 'deltavlos', 'deltaphi', 'Ratio', 
                      'Nadf', 'deltaadf', 'alphaB']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert integer columns
    int_columns = ['Bu_ref', 'Bu_est', 'Btot_est']
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    # Save processed data if requested
    if save_path:
        df.to_csv(save_path, index=False)
    
    return df

if __name__ == "__main__":

    import os
    from maguniverse import __parent_dir__

    output_path = os.path.join(
        __parent_dir__, 'datafiles', 'processed', 'liu2022_processed.csv'
    )
    src_data_path = os.path.join(
        __parent_dir__, 'datafiles', 'processed', 'liu2022.txt'
    )
    df = get_liu2022(save_path=output_path, save_src_data_path=src_data_path)
    print(df.head())
