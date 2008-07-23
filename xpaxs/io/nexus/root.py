"""
Wrappers around the pytables interface to the hdf5 file.

"""

from __future__ import absolute_import

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .entry import NXentry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class NXroot(NXentry):

    _protected = ('file_name', 'file_time', 'name', 'file_update_time')

    """
    """
