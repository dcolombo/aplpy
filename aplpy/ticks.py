from __future__ import absolute_import, print_function, division

import warnings

import numpy as np
from matplotlib.pyplot import Locator
import astropy.units as u

from . import angle_util as au
from . import scalar_util as su
from .decorators import auto_refresh


class Ticks(object):

    @auto_refresh
    def __init__(self, parent):
        self._ax = parent.ax
        self.x = parent.x
        self.y = parent.y
        self._wcs = self._ax.wcs

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parent._parameters

    @auto_refresh
    def set_xspacing(self, spacing):
        '''
        Set the x-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''
        self._set_spacing(self.x, spacing)

    @auto_refresh
    def set_yspacing(self, spacing):
        '''
        Set the y-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''
        self._set_spacing(self.y, spacing)

    @auto_refresh
    def _set_spacing(self, coord, spacing):
        if spacing == 'auto':
            self._ax.coords[coord].set_ticks(spacing=None)
        else:
            coord_unit = self._wcs.wcs.cunit[coord]

            coord_type = self._ax.coords[coord].coord_type
            format = self._ax.coords[coord]._formatter_locator.format
            if format is not None:
                if coord_type in ['longitude', 'latitude']:
                    try:
                        # TODO: Test this
                        au._check_format_spacing_consistency(format, au.Angle(degrees=spacing, latitude=coord_type == 'latitude'))
                    except au.InconsistentSpacing:
                        warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                        return
                else:
                    try:
                        # TODO: Test
                        su._check_format_spacing_consistency(format, spacing)
                    except au.InconsistentSpacing:
                        warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                        return
            self._ax.coords[coord].set_ticks(spacing=spacing * coord_unit)

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the ticks
        '''
        self._ax.coords[self.x].set_ticks(color=color)
        self._ax.coords[self.y].set_ticks(color=color)

    @auto_refresh
    def set_length(self, length, minor_factor=0.5):
        '''
        Set the length of the ticks (in points)
        '''
        # TODO: Can't set minor ticksize. Should we just remove that?
        # Not mentioned in the APLpy in docs either
        self._ax.coords[self.x].set_ticks(size=length)
        self._ax.coords[self.y].set_ticks(size=length)

    @auto_refresh
    def set_linewidth(self, linewidth):
        '''
        Set the linewidth of the ticks (in points)
        '''
        self._ax.coords[self.x].set_ticks(width=linewidth)
        self._ax.coords[self.y].set_ticks(width=linewidth)

    @auto_refresh
    def set_minor_frequency(self, frequency):
        '''
        Set the number of subticks per major tick. Set to one to hide minor
        ticks.
        '''
        self._ax.coords[self.x].set_minor_frequency(frequency)
        self._ax.coords[self.y].set_minor_frequency(frequency)

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis ticks
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis ticks
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_position('all')

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_position('')

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_position('all')

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_position('')
