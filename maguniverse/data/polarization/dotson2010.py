# -*- coding: utf-8 -*-
"""
dotson2010.py
----------

Functions for fetching and processing polarization data from Dotson et al. (2010) [1]_.

The paper presents polarization measurements of dust emission in various astronomical
objects.

Note
----
Due to potential CAPTCHA protection on the publisher's website, this module prefers
a local copy of the ASCII data file.

References
----------
.. [1] Dotson, J. L., Vaillancourt, J. E., Kirby, L., et al. (2010)
       350 μm Polarimetry from the Caltech Submillimeter Observatory.
       The Astrophysical Journal Supplement Series, 186(2), 406-426.
       DOI: 10.1088/0067-0049/186/2/406
"""

from io import StringIO
import pandas as pd

from maguniverse.data.polarization import polarization_sources
from maguniverse.utils import get_ascii, get_default_data_paths


def _get_table_config(table):
    """Get configuration for specified table type.

    Parameters
    ----------
    table : {'t1', 't2'}
        Which table to load.

    Returns
    -------
    dict
        Configuration dictionary containing:
        - column_names : list
            Names of columns in the table
        - skip_rows : int
            Number of header rows to skip
        - skip_footer : int
            Number of footer rows to skip
        - data_key_local : str
            Key to access local data path from polarization_sources
        - data_key_ascii : str
            Key to access ASCII data URL from polarization_sources
    """
    if table == 't1':
        return {
            'column_names': [
                'Source',
                'Runs',
                'alpha (2000)',         # (hh:mm:ss.s)
                'delta (2000)',         # (dd:mm:ss)
                'l',                    # (deg)
                'b',                    # (deg)
                'Chop Throw',           # (arcsec)
                'Chop Angle',           # (degrees E of N)
                'Peak Intensity',       # (Jy beam^-1)
                'Intensity Reference',  # reference number
                'Previously Published'
            ],
            'skip_rows': 6,
            'skip_footer': 9, 
            'data_key_local': 't1_object_list_local',
            'data_key_ascii': 't1_object_list_ascii'
        }
    else:  # table == 't2'
        return {
            'column_names': [
                'ID',
                'ΔR.A.',
                'ΔDecl.',
                'Δx',
                'Δy',
                'P',
                'sigma(P)',
                'theta',
                'sigma(theta)',
                'Intensity',
                'sigma(Intensity)',
                'Number of Observations'
            ],
            'skip_rows': 31,
            'skip_footer': 0,
            'data_key_local': 't2_data_table_local',
            'data_key_ascii': 't2_data_table_ascii'
        }


def get_dotson2010(file_path=None, file_url=None, save_path=None, 
                   save_src_data_path=None, table='t2'):
    """Load the Dotson et al. (2010) polarization measurements into a DataFrame.

    This function reads and processes the polarization data table from Dotson et al. (2010),
    which contains measurements of dust emission polarization.

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
    table : {'t1', 't2'}, optional
        Which table to load:
        - 't1': table 1 data
        - 't2': table 2 data (default)

    Returns
    -------
    pandas.DataFrame
        For table='t2' (default):
            A DataFrame containing the following columns:
            - ID : Measurement identification number
            - ΔR.A. : Right ascension offset (arcsec)
            - ΔDecl. : Declination offset (arcsec)
            - Δx : X-axis offset (arcsec)
            - Δy : Y-axis offset (arcsec)
            - P : Polarization percentage (%)
            - sigma(P) : Uncertainty in polarization percentage (%)
            - theta : Polarization angle (degrees)
            - sigma(theta) : Uncertainty in polarization angle (degrees)
            - Intensity : Measured intensity (units as in paper)
            - sigma(Intensity) : Uncertainty in intensity
            - Number of Observations : Number of independent measurements

        For table='t1':
            - Source : Source name
            - Runs : Run number
            - alpha (2000) : Right ascension (hh:mm:ss.s)
            - delta (2000) : Declination (dd:mm:ss)
            - l : Galactic longitude (deg)
            - b : Galactic latitude (deg)
            - Chop Throw : Chop throw (arcsec)
            - Chop Angle : Chop angle (degrees E of N)
            - Peak Intensity : Peak intensity (Jy beam^-1)
            - Intensity Reference : Reference number
            - Previously Published : Whether the source has been previously published

    Raises
    ------
    ValueError
        If table is not 't1' or 't2', or if both file_path and file_url are provided but point to different sources.
    TypeError
        If save_path or save_src_data_path are not strings when provided.
    """
    # Input validation
    if table not in ['t1', 't2']:
        raise ValueError("table must be either 't1' or 't2'")
    if save_path is not None and not isinstance(save_path, str):
        raise TypeError("save_path must be a string")
    if save_src_data_path is not None and not isinstance(save_src_data_path, str):
        raise TypeError("save_src_data_path must be a string")

    # Get table configuration
    config = _get_table_config(table)

    # Get default paths if none provided
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            polarization_sources['Dotson2010']['data_link'][config['data_key_local']],
            polarization_sources['Dotson2010']['data_link'][config['data_key_ascii']]
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')
 
    if table == 't1':
        # Table 1 has irregular spacing
        # Need to manually parse the data section
        lines = raw.split('\n')
        
        # Skip header and footer lines
        data_lines = lines[config['skip_rows']:len(lines)-config['skip_footer']]
        
        parsed_data = []
        current_row = {}
        
        for line in data_lines:
            line = line.rstrip()  # Keep leading tabs but remove trailing whitespace
            if not line.strip():  # Skip empty lines
                continue
            
            # Split by tabs but preserve the structure
            parts = line.split('\t')
            
            # Check if this is a new entry or continuation
            # NOTE: A continuation line starts with empty first field (just a tab)
            # TODO: Verify the interpretation of continuation lines, current continuation lines
            # are not being handled correctly.
            if parts[0].strip():  # Non-empty first column means new source
                # Save previous row if exists
                if current_row:
                    parsed_data.append(current_row)
                
                # Start new row - clean up parts and assign to columns
                current_row = {}
                for i, col_name in enumerate(config['column_names']):
                    if i < len(parts):
                        value = parts[i].strip() if parts[i] else None
                        current_row[col_name] = value if value else None
                    else:
                        current_row[col_name] = None
            else:
                # a continuation line - merge with current row
                # TODO: current continuation lines are not being handled correctly.
                if current_row and len(parts) > 1:
                    # Update fields that have data in this continuation line
                    for i, col_name in enumerate(config['column_names']):
                        if i < len(parts) and parts[i].strip():
                            value = parts[i].strip()
                            if current_row[col_name]:
                                # For runs, chop throw, chop angle - use semicolon
                                # TODO: Verify the interpretation of continuation lines, current continuation lines
                                # are not being handled correctly.
                                if col_name in ['Runs', 'Chop Throw', 'Chop Angle']:
                                    current_row[col_name] += f"; {value}"
                                else:
                                    current_row[col_name] = value
                            else:
                                current_row[col_name] = value
        
        if current_row: parsed_data.append(current_row)
        df = pd.DataFrame(parsed_data) 

    else:
        # table 2
        df = pd.read_csv(
            StringIO(raw),
            sep=r'\s+',         # Use regex to match whitespace
            names=config['column_names'],
            skiprows=config['skip_rows'],
            skipfooter=config['skip_footer'],
            engine='python'     # Required for skipfooter
        )

    # Save processed data if requested
    if save_path:
        df.to_csv(save_path, index=False)

    return df


if __name__ == "__main__":
    # Example usage - Table 1
    df_t1 = get_dotson2010(table='t1', save_path=r'datafiles\polarization\dotson2010t1_processed.txt')
    print("Table 1 data:")
    print(df_t1)
    
    # Example usage - Table 2 (default)
    df_t2 = get_dotson2010(table='t2', save_path=r'datafiles\polarization\dotson2010t2_processed.txt')
    print("\nTable 2 data:")
    print(df_t2.head())