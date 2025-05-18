# -*- coding: utf-8 -*-
"""
jijina1999.py
----------

Fetch and process the Jijina et al. (1999) Ammonia gas properties data.
J/ApJS/125/161

"""

from io import StringIO
import pandas as pd

from maguniverse.data.gas import gas_sources
from maguniverse.utils import get_ascii, get_default_data_paths

def get_jijina1999(file_path=None, file_url=None, save_path=None, save_src_data_path=None):
    """
    Load the Jijina et al. (1999) Ammonia gas properties data table into a DataFrame.

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
        'Seq',              # Database reference number
        'n_Seq',            # Note on Seq
        'Name',             # Name of the NH_3_(1,1) source
        'logNNH3 ([cm-2])', # Logarithm (log_10_) of the total NH_3_ column density
        'u_logNNH3',        # Uncertainty
        'DVint (km/s)',     # Intrinsic line widths
        'u_DVint',          # Uncertainty
        'Tkin (K)',         # Kinetic temperature
        'u_Tkin',           # Uncertainty
        'logNtot ([cm-3])', # Logarithm of the total volume density of the molecule of mean mass
        'u_logNtot',        # Uncertainty
        'R (pc)',           # Core size
        'u_R',              # Uncertainty
        'a/b'               # Projected aspect ratio
    """
    if file_path is None and file_url is None:
        file_path, file_url = get_default_data_paths(
            file_path,
            gas_sources['Jijina1999']['data_link']['t2_gas_properties']
        )

    # Fetch raw ASCII (prefers local copy to avoid CAPTCHA)
    raw = get_ascii(file_path, file_url, save_src_data_path, fmt='txt')

    # Define column names and read into DataFrame
    column_names = [
        'Seq',              # Database reference number
        'n_Seq',            # Note on Seq
        'Name',             # Name of the NH_3_(1,1) source
        'logNNH3 ([cm-2])', # Logarithm (log_10_) of the total NH_3_ column density
        'u_logNNH3',        # Uncertainty
        'DVint (km/s)',     # Intrinsic line widths
        'u_DVint',          # Uncertainty
        'Tkin (K)',         # Kinetic temperature
        'u_Tkin',           # Uncertainty
        'logNtot ([cm-3])', # Logarithm of the total volume density of the molecule of mean mass
        'u_logNtot',        # Uncertainty
        'R (pc)',           # Core size
        'u_R',              # Uncertainty
        'a/b'               # Projected aspect ratio
    ]
    colspecs = [
        (0,  3),  # Seq (I3)
        (4,  5),  # n_Seq (A1)
        (6, 22),  # Name (a16)
        (23, 27), # logNNH3 ([cm-2]) (F4.1)
        (28, 29), # u_logNNH3 (A1)
        (30, 35), # DVint (km/s) (F5.2)
        (36, 37), # u_DVint (A1)
        (38, 43), # Tkin (K) (F5.1)
        (44, 45), # u_Tkin (A1)
        (46, 50), # logNtot ([cm-3]) (F4.1)
        (51, 52), # u_logNtot (A1)
        (53, 58), # R (pc) (F5.2)
        (59, 60), # u_R (A1)
        (61, 65)  # a/b (F4.1)
    ]      
    df = pd.read_fwf(
        StringIO(raw),
        names=column_names,
        skiprows=55,
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
        __parent_dir__, 'datafiles/polarization/jijina1999_processed.txt'
    )
    src_data_path = os.path.join(
        __parent_dir__, 'datafiles/polarization/jijina1999.txt'
    )
    df = get_jijina1999(save_path=output_path, save_src_data_path=src_data_path)
    print(df.head())