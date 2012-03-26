#!/usr/bin/env python
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from pylab import *

def radar_factory(num_vars, frame='polygon'):
    """Create a radar chart with `num_vars` axes.
    """
    # calculate evenly-spaced axis angles
    theta = 2*pi * linspace(0, 1-1/float(num_vars), num_vars)
    # rotate theta such that the first axis is at the top
    theta += pi/2
    
    def draw_poly_frame(self, x0, y0, r):
        # TODO: should use transforms to convert (x, y) to (r, theta)
        verts = [(r*cos(t) + x0, r*sin(t) + y0) for t in theta]
        return Polygon(verts, closed=True)
        
    def draw_circle_frame(self, x0, y0, r):
        return Circle((x0, y0), r)
        
    frame_dict = {'polygon': draw_poly_frame, 'circle': draw_circle_frame}
    if frame not in frame_dict:
        raise ValueError, 'unknown value for `frame`: %s' % frame
    
    class RadarAxes(PolarAxes):
        """Class for creating a radar chart (a.k.a. a spider or star chart)
        
        http://en.wikipedia.org/wiki/Radar_chart
        """
        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_frame = frame_dict[frame]
        
        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)
            
        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
        
        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = concatenate((x, [x[0]]))
                y = concatenate((y, [y[0]]))
                line.set_data(x, y)
                
        def set_varlabels(self, labels):
            self.set_thetagrids(theta * 180/pi, labels)
            
        def get_axes_patch(self):
            x0, y0 = (0.5, 0.5)
            r = 0.5
            return self.draw_frame(x0, y0, r)
    register_projection(RadarAxes)
    
    return theta

if __name__ == '__main__':
    N = 5
    
    theta = radar_factory(N)
    # theta = radar_factory(N, frame='circle')
    
    ax = subplot(111, projection='radar')
    
    labels = ['humor', 'sarcasm', 'news content', 'America', 'overall']
    colbert   = [8, 9, 5, 9, 7]
    dailyshow = [9, 6, 8, 3, 9]
    
    # ax.plot(theta, dailyshow, 'b-o')
    # ax.plot(theta, colbert, 'r-s')
    
    ax.fill(theta, dailyshow, 'b')
    ax.fill(theta, colbert, 'r')
    for patch in ax.patches:
        patch.set_alpha(0.5)
    
    # FIXME: legend doesn't work when fill is called
    # ax.legend(['The Daily Show', 'Colbert Report'])

    ax.set_varlabels(labels)
    # FIXME: rgrid lines don't appear; works if RESOLUTION is increased.
    rgrids((2, 4, 6, 8, 10))

    grid(True)
    show()
