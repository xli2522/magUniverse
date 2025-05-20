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


def get_dotson2010(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
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

    Returns
    -------
    pandas.DataFrame
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

    # Save processed data if requested
    if save_path:
        df.to_csv(save_path, index=False)

    return df


if __name__ == "__main__":
    # Example usage
    df = get_dotson2010()
    print(df.head())