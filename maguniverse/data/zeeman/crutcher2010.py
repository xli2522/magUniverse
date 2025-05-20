# -*- coding: utf-8 -*-
"""
crutcher2010.py
----------

Functions for fetching and processing Zeeman effect data from Crutcher et al. (2010) [1]_.

The paper presents a comprehensive analysis of magnetic field strengths in molecular
clouds using Zeeman effect measurements.

Note
----
Due to CAPTCHA protection on the publisher's website, this module prefers
a local copy of the ASCII data file.

References
----------
.. [1] Crutcher, R. M., Wandelt, B., Heiles, C., Falgarone, E., & Troland, T. H. (2010)
       Magnetic Fields in Interstellar Clouds from Zeeman Observations: Inference of Total
       Field Strengths by Bayesian Analysis.
       The Astrophysical Journal, 725(1), 466-479.
       DOI: 10.1088/0004-637X/725/1/466
"""

from io import StringIO
import pandas as pd

from maguniverse.data.zeeman import zeeman_sources
from maguniverse.utils import get_ascii, get_default_data_paths


def get_crutcher2010(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """Load the Crutcher et al. (2010) Zeeman measurements into a DataFrame.

    This function reads and processes Table 1 from Crutcher et al. (2010), which contains
    Zeeman effect measurements of magnetic field strengths in molecular clouds.

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
        - Name : Source identification
        - Species : Molecular species used for Zeeman measurement
        - Ref : Reference number for the observation
        - n_H (cm^-3) : Number density of hydrogen
        - B_Z (muG) : Line-of-sight magnetic field strength (microGauss)
        - sigma (muG) : Uncertainty in B_Z measurement (microGauss)

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
            zeeman_sources['Crutcher2010']['data_link']['table1_local'],
            zeeman_sources['Crutcher2010']['data_link']['table1_ascii']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Define column names with descriptions
    column_names = [
        'Name',          # Source identification
        'Species',       # Molecular species used for Zeeman measurement
        'Ref',          # Reference number
        'n_H (cm^-3)',  # Number density of hydrogen
        'B_Z (muG)',    # Line-of-sight magnetic field strength
        'sigma (muG)'   # Uncertainty in B_Z measurement
    ]

    # Read data into DataFrame using tab-separated format
    df = pd.read_csv(
        StringIO(raw),
        sep=r'\t+',        # Match one or more tabs
        header=None,       # No header in file
        names=column_names,
        skiprows=5,        # Skip header rows
        skipfooter=3,      # Skip footer rows
        engine='python'    # Required for skipfooter
    )

    # Clean and process numeric columns
    numeric_cols = ['n_H (cm^-3)', 'B_Z (muG)']
    for col in numeric_cols:
        df[col] = (
            df[col].astype(str)
                   .str.replace(r'\s*x\s*10\^', 'e', regex=True)  # Convert scientific notation
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, invalid as NaN

    # Save processed data if requested
    if save_path:
        df.to_csv(save_path, index=False)

    return df


if __name__ == "__main__":
    """
    Example usage:

    >>> from maguniverse import __parent_dir__
    >>> import os

    >>> csv_path = os.path.join(
    >>>     __parent_dir__, 'datafiles/zeeman/crutcher2010_processed.txt'
    >>> )
    >>> df = get_crutcher2010(save_path=csv_path)
    >>> print(df.head())
    """
    import os
    from maguniverse import __parent_dir__

    output_path = os.path.join(
        __parent_dir__, 'datafiles/zeeman/crutcher2010_processed.txt'
    )
    df = get_crutcher2010(save_path=output_path)
    print(df.head())
