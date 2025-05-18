# -*- coding: utf-8 -*-
"""
matthews2009.py
----------

Fetch and process the Matthews et al. (2009) polarization data.

"""

from io import StringIO
import pandas as pd

from maguniverse.data.polarization import polarization_sources
from maguniverse.utils import get_ascii, get_default_data_paths

def get_matthews2009(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """
    Load the Matthews et al. (2009) polarization data table into a DataFrame.

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
    DataFrame
        Columns are:
        "ID",      # Object/Region identification
        "f_ID",    # [bc] Flag on ID (1)
        "RAOff",   # Offset in Right Ascension (2)
        "DEOff",   # Offset in Declination (2)
        "RAh",     # Hour of Right Ascension (J2000) 
        "RAm",     # Minute of Right Ascension (J2000) 
        "RAs",     # Second of Right Ascension (J2000)
        "DE-",     # Sign of the Declination (J2000)
        "DEd",     # Degree of Declination (J2000)
        "DEm",     # Arcminute of Declination (J2000)
        "DEs",     # Arcsecond of Declination (J2000)
        "Int",     # Intensity
        "e_Int",   # Error in Int
        "Pol",     # Polarization percentage
        "e_Pol",   # Error in Pol
        "theta",   # Polarization angle 
        "e_theta", # Error in theta
    """
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            file_path,
            polarization_sources['Matthews2009']['data_link']['t6_polarization']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Define column names and read into DataFrame
    column_names = [
        "ID",      # Object/Region identification
        "f_ID",    # [bc] Flag on ID (1)
        "RAOff",   # Offset in Right Ascension (2)
        "DEOff",   # Offset in Declination (2)
        "RAh",     # Hour of Right Ascension (J2000) 
        "RAm",     # Minute of Right Ascension (J2000) 
        "RAs",     # Second of Right Ascension (J2000)
        "DE-",     # Sign of the Declination (J2000)
        "DEd",     # Degree of Declination (J2000)
        "DEm",     # Arcminute of Declination (J2000)
        "DEs",     # Arcsecond of Declination (J2000)
        "Int",     # Intensity
        "e_Int",   # Error in Int
        "Pol",     # Polarization percentage
        "e_Pol",   # Error in Pol
        "theta",   # Polarization angle 
        "e_theta", # Error in theta
    ]
    colspecs = [
        (0, 12),   # 1–12
        (13, 14),  # 14
        (15, 21),  # 16–21
        (22, 28),  # bytes 23–28
        (29, 31),  # bytes 30–31
        (32, 34),  # bytes 33–34
        (35, 40),  # bytes 36–40
        (41, 42),  # byte    42
        (42, 44),  # bytes 43–44
        (45, 47),  # bytes 46–47
        (48, 52),  # bytes 49–52
        (53, 62),  # bytes 54–62
        (63, 72),  # bytes 64–72
        (73, 77),  # bytes 74–77
        (78, 81),  # bytes 79–81
        (82, 87),  # bytes 83–87
        (88, 92),  # bytes 89–92
    ]      
    df = pd.read_fwf(
        StringIO(raw),
        names=column_names,
        skiprows=31,
        colspecs=colspecs
    )

    if save_path:
        df.to_csv(save_path, index=False)

    return df

if __name__ == "__main__":
    # Example usage
    import os
    from maguniverse import __parent_dir__
    
    # this example demonstrates how to access a remote ascii file
    # and save the raw file and processed dataframe locally

    output_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/matthews2009_processed.txt'
    )
    src_data_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/matthews2009.txt'
    )
    df = get_matthews2009(save_path=output_path, save_src_data_path=src_data_path)
    print(df.head())