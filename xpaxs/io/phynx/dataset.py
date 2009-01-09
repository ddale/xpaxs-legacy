"""
"""

from __future__ import absolute_import, with_statement

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

from posixpath import basename

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

try:
    from enthought.traits.api import HasTraits
except ImportError:
    class HasTraits(object):
        pass
import h5py

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------

from .base import _PhynxProperties
from .registry import registry

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class Dataset(h5py.Dataset, _PhynxProperties, HasTraits):

    """
    """

    def __init__(self, parent_object, name, *args, **kwargs):
        with parent_object._lock:
            attrs = kwargs.pop('attrs', {})
            if name in parent_object:
                super(Dataset, self).__init__(
                    parent_object, name, *args, **kwargs
                )
            else:
                super(Dataset, self).__init__(
                    parent_object, name, *args, **kwargs
                )
                self.attrs['class'] = self.__class__.__name__

                _PhynxProperties.__init__(self, parent_object)

                for key, val in attrs.iteritems():
                    self.attrs[key] = val

    def __repr__(self):
        with self._lock:
            try:
                return '<%s dataset "%s": shape %s, type "%s" (%d attrs)>'%(
                    self.__class__.__name__,
                    self.name,
                    self.shape,
                    self.dtype.str,
                    len(self.attrs)
                )
            except Exception:
                return "<Closed %s dataset>" % self.__class__.__name__

    @property
    def name(self):
        return basename(super(Dataset, self).name)

    @property
    def path(self):
        return super(Dataset, self).name

registry.register(Dataset)


class Axis(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Axis)
                return cmp(self.primary, other.primary)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Axis and %s'%other.__class__.__name__
                )

    @property
    def axis(self):
        with self._lock:
            try:
                return self.attrs['axis']
            except h5py.H5Error:
                return 0

    @property
    def primary(self):
        with self._lock:
            try:
                return self.attrs['primary']
            except h5py.H5Error:
                return 0

    @property
    def range(self):
        with self._lock:
            try:
                temp = self.attrs['range'].lstrip('(').rstrip(')')
            except h5py.H5Error:
                temp = ''
            return tuple(temp.split(',')) if temp else tuple()

registry.register(Axis)


class Signal(Dataset):

    """
    """

    def __cmp__(self, other):
        with self._lock:
            try:
                assert isinstance(other, Signal)
                ss = self.signal if self.signal else 999
                os = other.signal if other.signal else 999
                return cmp(ss, os)
            except AssertionError:
                raise AssertionError(
                    'Cannot compare Signal and %s'%other.__class__.__name__
                )

    @property
    def signal(self):
        with self._lock:
            try:
                return self.attrs['signal']
            except h5py.H5Error:
                return 0

registry.register(Signal)
