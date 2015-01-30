#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   wuyanjun 00291783
#   E-mail  :   wu.wu@hisilicon.com
#   Date    :   15/01/23 18:38:11
#   Desc    :  
#
import matplotlib
matplotlib.use("Agg")

import os
import string
import yaml
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
import pdb

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with 'num_vars' axes.

    This function creates a RadarAxes projection and registers it.
    Parameters:
    num_vars: int   Number of variables for radar chart
    frame: {'circle' | 'polygon'}  Shape of frame surrounding axes.
    """
    # calculate evenly-spaced axis angles
    # nu, py.linespace(start, stop, num=50, endpoint=True, retstep=Falise, dtype=None)
    theta = 2 * np.pi * np.linspace(0, 1-1./num_vars, num_vars)

    # rotate theta such that the first axis is at the top
    theta += np.pi/2
    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='K')
   
    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):
        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that lines is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)
   
        def set_varlabels(self, labels):
            self.set_thetagrids(theta * 180/np.pi, labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame

            # spine_type must be 'left', 'right', 'top', 'bottom', or 'circle'
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}
    register_projection(RadarAxes)
    return theta

def unit_poly_verts(theta):
    """
    Return vertices of polygon for a subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def get_Items_score(files_list):
    targets_scores = []
    for i in range(0, len(files_list)):
        full_path = "/home/wuyanjun/caliper/gen/output/yaml"
        full_path_i = os.path.join(full_path, files_list[i])
        fp = open(full_path_i, 'r')
        result = yaml.load(fp)
        fp.close()
        subItems = result['results']['Performance']
        test_subItems = subItems.keys()
        scores_for_target = []
        for key in test_subItems:
            score = subItems[key]['Total_Scores']
            scores_for_target.append(string.atof(score))
        targets_scores.append(scores_for_target)
    return (test_subItems, targets_scores)

# get the apppropriate scale for each dimension for the spider diagram
def get_rgrids(data_lists):
    if len(data_lists) < 1:
        return []

    trans_data = [[d[col] for d in data_lists] for col in range(len(data_lists[0]))]
   
    rgrid_lists = []
    for i in range(0, len(trans_data)):
        tmp_max = max(trans_data[i])
        delta = tmp_max / len(trans_data)
        tmp_rgrids = []
        for j in range(0, len(trans_data)):
            tmp_rgrids.append( str( "%.2f"% (delta + j * delta) ) )
        rgrid_lists.append(tmp_rgrids)
    return rgrid_lists

def deal_data(data_lists):
    #   function: make the data in each dimension almostly near
    # the data_lists is planar
    max_of_matrix = data_lists[0][0]
    max_of_columns = []
    # i means the columns
    for i in range(0, len(data_lists[0])):
        tmp_max_column = data_lists[i][0]
        # j means the rows
        for j in range(0, len(data_lists)):
            if data_lists[j][i] > max_of_matrix:
                max_of_matrix = data_lists[j][i]
            if data_lists[j][i] > tmp_max_column:
                tmp_max_column = data_lists[j][i]
        max_of_columns.append(tmp_max_column)
   
    divisor_of_columns = [ max_of_matrix/data for data in max_of_columns ]
    for i in range(0, len(data_lists[0])):
        for j in range(0, len(data_lists)):
            data_lists[j][i] = data_lists[j][i] * divisor_of_columns[i]
    return data_lists

def draw_radar(file_lists, store_folder):
    (spoke_labels, data_lists) = get_Items_score(file_lists)
    dimension = len(spoke_labels)
    theta = radar_factory(dimension, frame='circle')
    labels = [file_list.split('_')[0] for file_list in file_lists]

    colors = ['b','r', 'g', 'm', 'y']
    if len(file_lists) < len(colors):
        colors = colors[0:len(file_lists)]
    title = 'Test Radar Diagram'

    pdb.set_trace()
    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    ax = fig.add_subplot(1, 1, 1, projection='radar')
    #for i in range(0, len(data_lists)):
    # get the approriate scale for the picture
    rgrid_list = get_rgrids(data_lists)

    #plt.rgrids( rgrid_list )
    ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                horizontalalignment='center', verticalalignment='center')
    angles_list = [ th*180/np.pi for th in theta ]
    angles = np.array(angles_list)
    length = len(rgrid_list)
    data = deal_data(data_lists)
   
    for d, color in zip(data, colors):
        ax.plot(theta, d, color=color)
        ax.fill(theta, d, facecolor=color, alpha=0.25)
  
    # FIXME: why can this work?
    #for angle, rgrid_data in zip(angles, rgrid_list):
    #    ax.set_rgrids(range(1, 1+length), angle=angle, labels=rgrid_data)
    ax.set_varlabels(spoke_labels)

    # the usage of subplot is plt.subplot(x, y, m)   m<=x*y
    plt.subplot(1, 1, 1)
    legend = plt.legend(labels, loc=(0.9, 0.95), labelspacing=0.1)
   
    plt.setp(legend.get_texts(), fontsize='small')
    plt.figtext(0.5, 0.965, 'Test of Drawing Radar Diagram for Caliper',
                ha='center', color='black', weight='bold', size='large')

    path_name = os.path.join(store_folder, "test.png")

    plt.savefig(path_name, dit=512)

if __name__ == "__main__":
    file_lists = ['D01_16_result.yaml', 'D01_1_result.yaml', 'Server_result.yaml',
                    'TV_result.yaml']
    picture_location = "/home/wuyanjun/caliper/gen/output/html"
    try:
        draw_radar(file_lists, picture_location)
    except Exception, e:
        raise e