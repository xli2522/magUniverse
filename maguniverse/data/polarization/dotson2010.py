# -*- coding: utf-8 -*-
"""
dotson2010.py
----------

Fetch and process the Dotson et al. (2010) polarization data.

Due to potential CAPTCHA protection on the publisher's website, this module prefers
a local copy of the ASCII data file.
"""

from io import StringIO
import pandas as pd

from maguniverse.data.polarization import polarization_sources
from maguniverse.utils import get_ascii, get_default_data_paths

def get_dotson2010(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """
    Load the Dotson et al. (2010) polarization measurements into a DataFrame.

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
    """
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            polarization_sources['Dotson2010']['data_link']['t2_data_table_local'],
            polarization_sources['Dotson2010']['data_link']['t2_data_table_ascii']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Define column names and read into DataFrame
    column_names = [
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
    ]
    df = pd.read_csv(
        StringIO(raw),
        sep=r'\s+',         # Use regex to match whitespace
        names=column_names,
        skiprows=31,        # Skip the header
    )

    if save_path:
        df.to_csv(save_path, index=False)

    return df

if __name__ == "__main__":
    # Example usage
    df = get_dotson2010()
    print(df.head())