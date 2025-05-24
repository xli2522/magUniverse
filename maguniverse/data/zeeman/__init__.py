from maguniverse.data.zeeman.crutcher2010 import get_crutcher2010

__all__ = [ "zeeman_sources",
            "get_crutcher2010"]

zeeman_sources = {
    "Crutcher2010": {
        "title"     : "Magnetic Fields in Interstellar Clouds from Zeeman Observations: Inference of Total Field Strengths by Bayesian Analysis",
        "authors"   : "Richard M. Crutcher, Benjamin Wandelt, Carl Heiles, Edith Falgarone, and Thomas H. Troland",
        "year"      : 2010,
        "publisher_link": "https://iopscience.iop.org/article/10.1088/0004-637X/725/1/466",
        "ads_link"  : "https://ui.adsabs.harvard.edu/abs/2010ApJ...725..466C/abstract",
        "doi"       : "10.1088/0004-637X/725/1/466",
        "instrument": "Compilation of HI, OH, and CN Zeeman measurements",
        "note"      : "This table compiles four earlier surveys (Heiles & Troland 2004; Crutcher et al. 1999; Troland & Crutcher 2008; Falgarone et al. 2008)",
        "data_link" : {
            "table1_ascii": "https://iopscience.iop.org/0004-637X/725/1/466/suppdata/apj333303t1_ascii.txt?doi=10.1088/0004-637X/725/1/466",
            "table1_local": "datafiles/zeeman/crutcher2010.txt",
        },
    },
}