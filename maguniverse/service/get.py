# -*- coding: utf-8 -*-
import inspect
from maguniverse.data import (zeeman_sources, polarization_sources, gas_sources)
from maguniverse.data.polarization  import (get_dotson2010,
                                            get_harris2018,
                                            get_matthews2009,)
from maguniverse.data.zeeman        import (get_crutcher2010,)
from maguniverse.data.gas           import (get_jijina1999, )

class getters():
    def __init__(self, env='others'):
        if env == 'pyodide':
            self.proxy = "https://api.allorigins.win/raw?url="
            self.session_dir = 'user_data/'
        else:
            self.proxy = ''
            self.session_dir = 'datafiles/'

        return 
    # session_dir, proxy

    def dotson2010_t2(self): return get_dotson2010(
                file_url=self.proxy+polarization_sources['Dotson2010']['data_link']['t2_data_table_ascii'], 
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt')
    
    def harris2018_t2(self): return get_harris2018(
                file_url=self.proxy+polarization_sources['Harris2018']['data_link']['t2_plane_fitting'], 
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt', 
                table='t2')
    
    def harris2018_t3(self): return get_harris2018(
                file_url=self.proxy+polarization_sources['Harris2018']['data_link']['t3_polarization'], 
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt', 
                table='t3')
    
    def matthews2009_t6(self): return get_matthews2009(
                file_url=self.proxy+polarization_sources['Matthews2009']['data_link']['t6_polarization'],
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt')
    
    def crutcher2010_t1(self): return get_crutcher2010(
                file_url=self.proxy+zeeman_sources['Crutcher2010']['data_link']['table1_ascii'], 
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt')
    
    def jijina1999_t2(self): return get_jijina1999(
                file_url=self.proxy+gas_sources['Jijina1999']['data_link']['t2_gas_properties'], 
                save_path=self.session_dir+inspect.stack()[0][3]+'.txt')


