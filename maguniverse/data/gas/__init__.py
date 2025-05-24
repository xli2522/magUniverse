from maguniverse.data.gas.jijina1999 import get_jijina1999

__all__ = [ "gas_sources",
            "get_jijina1999"]

gas_sources = {
    "Jijina1999": {
        "title"     : "Dense Cores Mapped in Ammonia: A Database",
        "authors"   : "J. Jijina, P. C. Myers, and Fred C. Adams",
        "year"      : 1999,
        "publisher_link": "https://iopscience.iop.org/article/10.1086/313268",
        "ads_link"  : "https://ui.adsabs.harvard.edu/abs/1999ApJS..125..161J/abstract",
        "doi"       : "10.1086/313268",
        "instrument": "",
        "data_link" : {
            "CDS"   : "https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/125/161",
            "t1_targets"        :   "https://vizier.cds.unistra.fr/viz-bin/asu-txt?-oc.form=sexa&-out.max=unlimited&-c.eq=J2000&-c.r=  2&-c.u=arcmin&-c.geom=r&-source=J/ApJS/125/161/tablea1&-order=I&-out=Seq&-out=n_Seq&-out=Name&-out=RA1950&-out=DE1950&-out=Tel&-out=SFR&-out=_RA.icrs&-out=_DE.icrs&",
            "t2_gas_properties" :   "https://vizier.cds.unistra.fr/viz-bin/asu-txt?-oc.form=sexa&-out.max=unlimited&-source=J/ApJS/125/161/tablea2&-order=I&-out=Seq&-out=n_Seq&-out=Name&-out=logNNH3&-out=u_logNNH3&-out=DVint&-out=u_DVint&-out=Tkin&-out=u_Tkin&-out=logNtot&-out=u_logNtot&-out=R&-out=u_R&-out=a/b&",
            "t3_yso_properties" :   "https://vizier.cds.unistra.fr/viz-bin/asu-txt?-oc.form=sexa&-out.max=50&-source=J/ApJS/125/161/tablea3&-order=I&-out=Seq&-out=n_Seq&-out=Name&-out=IRAS&-out=l_log(Liras)&-out=log(Liras)&-out=u_log(Liras)&-out=Dist&-out=n_Dist&-out=Vout&-out=n_Vout&-out=NIRAS&-out=n_NIRAS&",
        },
    },
}