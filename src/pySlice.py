#!/usr/bin/python

"""
The MIT License (MIT)
pySlice.py
Copyright (c) 2013 Matthew Else
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os

import errno

from Model3D import STLModel, Vector3, Normal

from operator import itemgetter

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

# @profile
def slice_file(f=None, resolution=0.1):
    print("Status: Loading File.")

    model = STLModel(f)
    scale = 10
    stats = model.stats()

    sub_vertex = Vector3(stats['extents']['x']['lower'], stats['extents']['y']['lower'], stats['extents']['z']['lower'])
    add_vertex = Vector3(0.5, 0.5, 0.5)

    model.xmin = model.xmax = None
    model.ymin = model.ymax = None
    model.zmin = model.zmax = None

    print("Status: Scaling Triangles.")

    for triangle in model.triangles:
        triangle.vertices[0] -= sub_vertex
        triangle.vertices[1] -= sub_vertex
        triangle.vertices[2] -= sub_vertex

        # The lines above have no effect on the normal.

        triangle.vertices[0] = (triangle.vertices[0] * scale) + add_vertex
        triangle.vertices[1] = (triangle.vertices[1] * scale) + add_vertex
        triangle.vertices[2] = (triangle.vertices[2] * scale) + add_vertex

        # Recalculate the triangle normal

        u = model.triangles[0].vertices[1] - model.triangles[0].vertices[0]
        v = model.triangles[0].vertices[2] - model.triangles[0].vertices[0]

        triangle.n = Normal((u.y * v.z) - (u.z * v.y), (u.z * v.x) - (u.x * v.z), (u.x * v.y) - (u.y * v.x))
        model.update_extents(triangle)

    print("Status: Calculating Slices")

    interval = scale * resolution
    stats = model.stats()

    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    slices = []
    for targetz in range(0, int(stats['extents']['z']['upper']), int(interval)):
        layer = model.slice_at_z(targetz)
        for line in layer:
            tmp_max_x = max(line, key=itemgetter(0))[0]
            tmp_max_y = max(line, key=itemgetter(1))[1]
            tmp_min_x = min(line, key=itemgetter(0))[0]
            tmp_min_y = min(line, key=itemgetter(1))[1]
            max_x = tmp_max_x if tmp_max_x > max_x else max_x
            max_y = tmp_max_y if tmp_max_y > max_y else max_y
            min_x = tmp_min_x if tmp_min_x < min_x else min_x
            min_y = tmp_min_y if tmp_min_y < min_y else min_y

        slices.append(layer)

    fig = {
        'min': {
            'x': min_x,
            'y': min_y
        },
        'max': {
            'x': max_x,
            'y': max_y
        },
        'slices': slices
    }

    import pickle
    filename = '../outputs/pkl/slices.pkl'

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'wb') as output:
        pickle.dump(fig, output)
