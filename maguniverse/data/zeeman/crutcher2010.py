# -*- coding: utf-8 -*-
"""
crutcher2010.py
----------

Fetch and process the Crutcher et al. (2010) Zeeman data.

Due to CAPTCHA protection on the publisher's website, this module prefers
a local copy of the ASCII data file.
"""

from io import StringIO
import pandas as pd

from maguniverse.data.zeeman import zeeman_sources
from maguniverse.utils import get_ascii, get_default_data_paths


def get_crutcher2010(file_path=None, file_url=None, save_path=None):
    """
    Load the Crutcher et al. (2010) Zeeman measurements into a DataFrame.

    Parameters
    ----------
    file_path : str, optional
        Local filesystem path to the ASCII data. If None, defaults are used.
    file_url : str, optional
        URL to download the ASCII data. If None, defaults are used.
    save_path : str, optional
        If provided, the resulting DataFrame is written to this CSV path.

    Returns
    -------
    DataFrame
        Columns are:
        - 'Name'
        - 'Species'
        - 'Ref'
        - 'n_H (cm^-3)'
        - 'B_Z (muG)'
        - 'sigma (muG)'
    """
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            zeeman_sources['Crutcher2010']['data_link']['table1_local'],
            zeeman_sources['Crutcher2010']['data_link']['table1_ascii']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, fmt='txt')

    # Define column names and read into DataFrame
    column_names = [
        'Name',
        'Species',
        'Ref',
        'n_H (cm^-3)',
        'B_Z (muG)',
        'sigma (muG)'
    ]

    df = pd.read_csv(
        StringIO(raw),
        sep=r'\t+',
        header=None,
        names=column_names,
        skiprows=5,
        skipfooter=3,
        engine='python'
    )

    # Clean and coerce numeric columns
    for col in ['n_H (cm^-3)', 'B_Z (muG)']:
        df[col] = (
            df[col].astype(str)
                #    .replace('nan', 'Nan')
                   .str.replace(r'\s*x\s*10\^', 'e', regex=True)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

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
