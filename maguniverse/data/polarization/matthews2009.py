# -*- coding: utf-8 -*-
"""
matthews2009.py
----------

Functions for fetching and processing polarization data from Matthews et al. (2009) [1]_.

The paper presents submillimeter polarization measurements of 83 regions, including
Bok globule (BG), starless or prestellar core (SC/PC), star-forming region (SFR), 
young stellar object (YSO), post-asymptotic giant branch star (AGB), planetary nebula (PN), 
supernova remnant (SNR), external galaxy (GAL), or the Galactic center (GC).

Note
----
Due to potential CAPTCHA protection on the publisher's website, this module prefers
a local copy of the ASCII data file.

References
----------
.. [1] Matthews, B. C., McPhee, C. A., Fissel, L. M., & Curran, R. L. (2009)
       The Legacy of SCUPOL: 850 μm Imaging Polarimetry from 1997 to 2005.
       The Astrophysical Journal Supplement Series, 182(1), 143-204.
       DOI: 10.1088/0067-0049/182/1/143
"""

from io import StringIO
import pandas as pd

from maguniverse.data.polarization import polarization_sources
from maguniverse.utils import get_ascii, get_default_data_paths


def get_matthews2009(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """Load the Matthews et al. (2009) polarization data table into a DataFrame.

    This function reads and processes Table 6 from Matthews et al. (2009), which contains
    submillimeter polarization measurements of 83 regions, including Bok globules and other sources.

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
        - ID : Object/Region identification
        - f_ID : Flag on ID ([bc] notation)
        - RAOff : Offset in Right Ascension (arcsec)
        - DEOff : Offset in Declination (arcsec)
        - RAh : Hour of Right Ascension (J2000)
        - RAm : Minute of Right Ascension (J2000)
        - RAs : Second of Right Ascension (J2000)
        - DE- : Sign of the Declination (J2000)
        - DEd : Degree of Declination (J2000)
        - DEm : Arcminute of Declination (J2000)
        - DEs : Arcsecond of Declination (J2000)
        - Int : Total intensity (Jy/beam)
        - e_Int : Uncertainty in intensity (Jy/beam)
        - Pol : Polarization percentage (%)
        - e_Pol : Uncertainty in polarization (%)
        - theta : Polarization angle (degrees E of N)
        - e_theta : Uncertainty in polarization angle (degrees)

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
            file_path,
            polarization_sources['Matthews2009']['data_link']['t6_polarization']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Define column specifications for fixed-width format
    column_names = [
        "ID",      # Object/Region identification
        "f_ID",    # [bc] Flag on ID
        "RAOff",   # Offset in Right Ascension
        "DEOff",   # Offset in Declination
        "RAh",     # Hour of Right Ascension (J2000)
        "RAm",     # Minute of Right Ascension (J2000)
        "RAs",     # Second of Right Ascension (J2000)
        "DE-",     # Sign of the Declination (J2000)
        "DEd",     # Degree of Declination (J2000)
        "DEm",     # Arcminute of Declination (J2000)
        "DEs",     # Arcsecond of Declination (J2000)
        "Int",     # Total intensity
        "e_Int",   # Error in intensity
        "Pol",     # Polarization percentage
        "e_Pol",   # Error in polarization
        "theta",   # Polarization angle
        "e_theta", # Error in theta
    ]
    
    # Column specifications based on byte positions in ASCII file
    colspecs = [
        (0, 12),   # ID: bytes 1-12
        (13, 14),  # f_ID: byte 14
        (15, 21),  # RAOff: bytes 16-21
        (22, 28),  # DEOff: bytes 23-28
        (29, 31),  # RAh: bytes 30-31
        (32, 34),  # RAm: bytes 33-34
        (35, 40),  # RAs: bytes 36-40
        (41, 42),  # DE-: byte 42
        (42, 44),  # DEd: bytes 43-44
        (45, 47),  # DEm: bytes 46-47
        (48, 52),  # DEs: bytes 49-52
        (53, 62),  # Int: bytes 54-62
        (63, 72),  # e_Int: bytes 64-72
        (73, 77),  # Pol: bytes 74-77
        (78, 81),  # e_Pol: bytes 79-81
        (82, 87),  # theta: bytes 83-87
        (88, 92),  # e_theta: bytes 89-92
    ]      

    # Read fixed-width formatted data
    df = pd.read_fwf(
        StringIO(raw),
        names=column_names,
        skiprows=31,  # Skip header rows
        colspecs=colspecs
    )

    # Save processed data if requested
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