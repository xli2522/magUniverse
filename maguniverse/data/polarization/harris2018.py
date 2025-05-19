# -*- coding: utf-8 -*-
"""
harris2018.py
----------

Functions for fetching and processing data from Harris et al. (2018) [1]_.

The paper presents ALMA observations of polarized 872μm dust emission from the
protostellar systems VLA 1623 and L1527.

Note
----
Due to potential CAPTCHA protection on the publisher's website, you may need to obtain a local copy
of the data tables.

References
----------
.. [1] Harris, R. J., Cox, E. G., Looney, L. W., et al. (2018)
       ALMA Observations of Polarized 872μm Dust Emission from the Protostellar
       Systems VLA 1623 and L1527. The Astrophysical Journal, 861(2), 91.
       DOI: 10.3847/1538-4357/aac6ec
"""

from io import StringIO
import pandas as pd

from maguniverse.data.polarization import polarization_sources
from maguniverse.utils import get_ascii, get_default_data_paths


def _get_table_config(table):
    """Get configuration for specified table type.

    Parameters
    ----------
    table : {'t2', 't3'}
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
        - data_key : str
            Key to access data URL from polarization_sources
    """
    if table == 't3':
        return {
            'column_names': [
                "Star",         # Source name
                "theta",        # Polarization angle (degrees)
                "phi",          # Minor-axis position angle (degrees)
                "|theta-phi|",  # Angle between theta and phi (degrees)
            ],
            'skip_rows': 6,
            'skip_footer': 1,
            'data_key': 't3_polarization'
        }
    else:  # table == 't2'
        return {
            'column_names': [
                "Weighting",    # Weighting type (Natural/Briggs/100 klambda)
                "Object",       # Source name
                "RA",           # Right Ascension (J2000)
                "Dec",          # Declination (J2000)
                "Ellipse Size", # Ellipse size (arcsec)
                "PA",           # Position angle (degrees)
                "I_peak",       # Peak intensity (mJy/beam)
                "I_int",        # Integrated intensity (mJy)
                "P_peak",       # Peak polarized intensity (mJy/beam)
                "P_int",        # Integrated polarized intensity (mJy)
            ],
            'skip_rows': 6,
            'skip_footer': 2,
            'data_key': 't2_plane_fitting'
        }


def get_harris2018(file_path=None, file_url=None, save_path=None, 
                   save_src_data_path=None, table='t3'):
    """Load Harris et al. (2018) data tables into a DataFrame.

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
    table : {'t3', 't2'}, optional
        Which table to load:
        - 't3': polarization data (default)
        - 't2': plane fitting data

    Returns
    -------
    pandas.DataFrame
        For table='t3' (default):
            Star        : Source name
            theta       : Polarization angle (degrees)
            phi         : Minor-axis position angle (degrees)
            |theta-phi| : Angle between theta and phi (degrees)

        For table='t2':
            Weighting   : Weighting type (Natural/Briggs/100 klambda)
            Object      : Source name
            RA          : Right Ascension (J2000)
            Dec         : Declination (J2000)
            Ellipse Size: Ellipse size (arcsec)
            PA          : Position angle (degrees)
            I_peak      : Peak intensity (mJy/beam)
            I_int       : Integrated intensity (mJy)
            P_peak      : Peak polarized intensity (mJy/beam)
            P_int       : Integrated polarized intensity (mJy)

    Raises
    ------
    ValueError
        If table is not 't2' or 't3'.
    """
    if table not in ['t2', 't3']:
        raise ValueError("table must be either 't2' or 't3'")

    # Get table configuration
    config = _get_table_config(table)

    # Get data path
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            file_path,
            polarization_sources['Harris2018']['data_link'][config['data_key']]
        )

    # Fetch raw ASCII data
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Read data into DataFrame
    df = pd.read_csv(
        StringIO(raw),
        sep=r'\t',
        names=config['column_names'],
        skiprows=config['skip_rows'],
        skipfooter=config['skip_footer'],
    )

    # Post-process table 2 data
    if table == 't2':
        # Fix alignment of specific rows
        rows_to_shift = [1, 2, 3, 5, 6]
        df.iloc[rows_to_shift, :] = df.iloc[rows_to_shift, :].shift(periods=1, axis=1)

    # Save processed data if requested
    if save_path:
        df.to_csv(save_path, index=False)

    return df


if __name__ == "__main__":
    import os
    from maguniverse import __parent_dir__

    # Example 1: Get polarization data (default)
    output_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/harris2018_t3_processed.txt'
    )
    src_data_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/harris2018_t3.txt'
    )
    df_pol = get_harris2018(file_url=polarization_sources['Harris2018']['data_link']['t2_plane_fitting'], 
                            save_path=output_path, 
                            table='t3')
    print("Polarization data:")
    print(df_pol.head())

    # Example 2: Get plane fitting data
    output_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/harris2018_t2_processed.txt'
    )
    src_data_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/harris2018_t2.txt'
    )
    df_plane = get_harris2018(file_url=polarization_sources['Harris2018']['data_link']['t2_plane_fitting'], 
                              table='t2', 
                              save_path=output_path)
    print("\nPlane fitting data:")
    print(df_plane.head())
