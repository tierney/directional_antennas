#!/usr/bin/env python

import numpy as N
import matplotlib.pyplot as P

from matplotlib.projections import PolarAxes, register_projection
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform

class NorthPolarAxes(PolarAxes):
    '''
    A variant of PolarAxes where theta starts pointing north and goes
    clockwise.
    '''
    name = 'northpolar'

    class NorthPolarTransform(PolarAxes.PolarTransform):
        def transform(self, tr):
            xy   = N.zeros(tr.shape, N.float_)
            t    = tr[:, 0:1]
            r    = tr[:, 1:2]
            x    = xy[:, 0:1]
            y    = xy[:, 1:2]
            x[:] = r * N.sin(t)
            y[:] = r * N.cos(t)
            return xy

        transform_non_affine = transform

        def inverted(self):
            return InvertedNorthPolarTransform()

    class InvertedNorthPolarTransform(PolarAxes.InvertedPolarTransform):
        def transform(self, xy):
            x = xy[:, 0:1]
            y = xy[:, 1:]
            r = N.sqrt(x*x + y*y)
            theta = N.arctan2(y, x)
            return N.concatenate((theta, r), 1)

        def inverted(self):
            return NorthPolarTransform()

    def _set_lim_and_transforms(self):
        PolarAxes._set_lim_and_transforms(self)
        self.transProjection = self.NorthPolarTransform()
        self.transData = (
            self.transScale + 
            self.transProjection + 
            (self.transProjectionAffine + self.transAxes))
        self._xaxis_transform = (
            self.transProjection +
            self.PolarAffine(IdentityTransform(), Bbox.unit()) +
            self.transAxes)
        self._xaxis_text1_transform = (
            self._theta_label1_position +
            self._xaxis_transform)
        self._yaxis_transform = (
            Affine2D().scale(N.pi * 2.0, 1.0) +
            self.transData)
        self._yaxis_text1_transform = (
            self._r_label1_position +
            Affine2D().scale(1.0 / 360.0, 1.0) +
            self._yaxis_transform)

register_projection(NorthPolarAxes)

# myd = [(0, 22.67157894736842),
#            (10, 23.756578947368421),
#            (20, 23.092039800995025),
#            (30, 24.081081081081081),
#            (40, 20.427450980392155),
#            (50, 17.668831168831169),
#            (60, 18.326599326599325),
#            (70, 17.487864077669904),
#            (80, 11.759776536312849),
#            (90, 15.906474820143885),
#            (100, 10.76),
#            (180, 22.90295358649789),
#            (190, 15.840220385674931),
#            (200, 23.93734939759036),
#            (210, 22.654794520547945),
#            (220, 19.866220735785951),
#            (230, 22.635730858468676),
#            (240, 12.791428571428572),
#            (250, 22.978401727861772),
#            (260, 24.961290322580645),
#            (270, 25.101052631578948),
#            (280, 20.38372093023256)]

# import math
# theta = [2*math.pi*i[0]/360. for i in myd]
# r     = [i[1] for i in myd]

# P.clf()
# P.subplot(1,1,1,projection='northpolar')
# P.plot(theta,r)
# P.show()
