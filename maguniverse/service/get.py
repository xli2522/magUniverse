# -*- coding: utf-8 -*-
import inspect
import logging
import pandas as pd
from maguniverse.data import (zeeman_sources, polarization_sources, gas_sources)
# Note: lazy import data getters

class getters():
    def __init__(self, env='others', datafile_path=None) -> None:
                    # Define multiple proxy options for fallback
        self.proxy_options = [
            # "",  # Direct access (no proxy)
            # "https://api.allorigins.win/raw?url=", 
            # "https://cors.bridged.cc/",  # CORS bridged
            # "https://cors.x2u.in/",  # India
            "https://api.codetabs.com/v1/proxy?quest=",
        ]
        if env == 'pyodide':
            self.session_dir = 'user_data/'
        else:
            self.session_dir = datafile_path if datafile_path is not None else 'datafiles/'
            import os
            os.makedirs(self.session_dir, exist_ok=True)


        # Set up logging for debugging proxy attempts
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Configure console handler for pyodide environment
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        return

    def configure_proxies(self, proxy_list) -> None:
        """
        Configure custom proxy options.
        
        Parameters
        ----------
        proxy_list : list
            List of proxy URLs to use. Include "" for direct access.
        """
        self.proxy_options = proxy_list
        self.logger.info(f"Updated proxy configuration with {len(proxy_list)} options")

    def _try_with_proxy_fallback(self, data_fetcher, data_source, table_key, **kwargs) -> pd.DataFrame:
        """
        Try to fetch data using multiple proxy options until successful or all options exhausted.
        
        Parameters
        ----------
        data_fetcher : function
            The data fetching function (e.g., get_dotson2010)
        data_source : dict
            The data source dictionary containing URLs
        table_key : str
            The key for the specific table URL in the data source
        **kwargs : dict
            Additional keyword arguments to pass to the data fetcher
            
        Returns
        -------
        DataFrame
            The fetched data
            
        Raises
        ------
        Exception
            If all proxy options fail
        """
        original_url = data_source['data_link'][table_key]
        last_exception = None
        
        self.logger.info(f"Starting proxy fallback for: {original_url}")
        
        for i, proxy in enumerate(self.proxy_options):
            proxy_name = "direct access" if not proxy else f"proxy {i}: {proxy.split('//')[1].split('/')[0]}"
            try:
                # Construct the URL with the current proxy
                file_url = proxy + original_url if proxy else original_url
                
                self.logger.info(f"Attempt {i+1}/{len(self.proxy_options)}: Trying {proxy_name}")
                
                # Attempt to fetch the data
                result = data_fetcher(file_url=file_url, **kwargs)
                
                self.logger.info(f"✓ SUCCESS with {proxy_name}!")
                return result
                
            except Exception as e:
                last_exception = e
                error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
                self.logger.warning(f"✗ Failed with {proxy_name}: {error_msg}")
                
                # If this is not the last option, continue to next proxy
                if i < len(self.proxy_options) - 1:
                    continue
        
        # If we get here, all proxy options failed
        error_msg = (f"All {len(self.proxy_options)} proxy options failed for {original_url}. "
                    f"Last error: {str(last_exception)}")
        self.logger.error(error_msg)
        raise Exception(error_msg)

    def dotson2010_t2(self) -> pd.DataFrame: 
        from maguniverse.data.polarization  import get_dotson2010
        return self._try_with_proxy_fallback(
            data_fetcher=get_dotson2010,
            data_source=polarization_sources['Dotson2010'],
            table_key='t2_data_table_ascii',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt'
        )
    
    def harris2018_t2(self) -> pd.DataFrame: 
        from maguniverse.data.polarization  import get_harris2018
        return self._try_with_proxy_fallback(
            data_fetcher=get_harris2018,
            data_source=polarization_sources['Harris2018'],
            table_key='t2_plane_fitting',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt',
            table='t2'
        )
    
    def harris2018_t3(self) -> pd.DataFrame: 
        from maguniverse.data.polarization  import get_harris2018
        return self._try_with_proxy_fallback(
            data_fetcher=get_harris2018,
            data_source=polarization_sources['Harris2018'],
            table_key='t3_polarization',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt',
            table='t3'
        )
    
    def matthews2009_t6(self) -> pd.DataFrame: 
        from maguniverse.data.polarization  import get_matthews2009
        return self._try_with_proxy_fallback(
            data_fetcher=get_matthews2009,
            data_source=polarization_sources['Matthews2009'],
            table_key='t6_polarization',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt'
        )
    
    def crutcher2010_t1(self) -> pd.DataFrame: 
        from maguniverse.data.zeeman  import get_crutcher2010
        return self._try_with_proxy_fallback(
            data_fetcher=get_crutcher2010,
            data_source=zeeman_sources['Crutcher2010'],
            table_key='table1_ascii',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt'
        )
    
    def jijina1999_t2(self) -> pd.DataFrame: 
        from maguniverse.data.gas  import get_jijina1999
        return self._try_with_proxy_fallback(
            data_fetcher=get_jijina1999,
            data_source=gas_sources['Jijina1999'],
            table_key='t2_gas_properties',
            save_path=self.session_dir+inspect.stack()[0][3]+'.txt'
        )


