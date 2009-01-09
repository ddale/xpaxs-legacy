
from __future__ import with_statement

import h5py

# TODO: use attrs.get() with h5py-1.1

class _PhynxProperties:

    """A mix-in class to propagate attributes from the parent object to
    the new HDF5 group or dataset, and to expose those attributes via
    python properties.
    """

    def __init__(self, parent_object):
        for attr in [
            'acquisition_shape', 'file_name', 'acquisition_name',
            'acquisition_id', 'npoints', 'format_version'
        ]:
            try:
                self.attrs[attr] = parent_object.attrs[attr]
            except h5py.H5Error:
                pass

    @property
    def format_version(self):
        if 'format_version' in self.attrs:
            return self.attrs['format_version']
        else:
            return ''

    @property
    def acquisition_shape(self):
        with self._lock:
            try:
                temp = self.attrs['acquisition_shape'].lstrip('(').rstrip(')')
            except h5py.H5Error:
                temp = ''
            return tuple(int(i) for i in temp.split(',')) if temp else tuple()

    @property
    def acquisition_id(self):
        with self._lock:
            try:
                return self.attrs['acquisition_id']
            except h5py.H5Error:
                return ''

    @property
    def acquisition_command(self):
        with self._lock:
            try:
                return self.attrs['acquisition_command']
            except h5py.H5Error:
                return ''

    @property
    def file_name(self):
        with self._lock:
            try:
                return self.attrs['file_name']
            except h5py.H5Error:
                return ''

    @property
    def npoints(self):
        with self._lock:
            try:
                return self.attrs['npoints']
            except h5py.H5Error:
                return 0
