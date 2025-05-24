# paper sources
from maguniverse.data.polarization.sources import polarization_sources
# getters
from maguniverse.data.polarization.dotson2010 import get_dotson2010
from maguniverse.data.polarization.matthews2009 import get_matthews2009
from maguniverse.data.polarization.harris2018 import get_harris2018

__all__ = [ "polarization_sources",
            "get_dotson2010",
            "get_matthews2009",
            "get_harris2018"]

