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
from Model3D import STLModel, Vector3, Normal
from svgwrite import Drawing, rgb
import pygame
import sys


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

    slices = []
    for targetz in range(0, int(stats['extents']['z']['upper']), int(interval)):
        layer = model.slice_at_z(targetz)
        slices.append(layer)

    import pickle
    output = open('outputs/stl/slices.pkl', 'wb')
    pickle.dump(slices, output)
    output.close()


    # ##########################
    # pygame.init()
    # size = [900, 600]
    # screen = pygame.display.set_mode(size)
    #
    # # Loop until the user clicks the close button.
    # done = False
    # clock = pygame.time.Clock()
    #
    # while not done:
    #
    #     # This limits the while loop to a max of 10 times per second.
    #     # Leave this out and we will use all CPU we can.
    #     clock.tick(40)
    #
    #     for event in pygame.event.get():  # User did something
    #         if event.type == pygame.QUIT:  # If user clicked close
    #             done = True  # Flag that we are done so we exit this loop
    #
    #     for layer in slices:
    #         screen.fill(BLACK)
    #         for pair in layer:
    #             pygame.draw.line(screen, WHITE, pair[0], pair[1], 5)
    #         pygame.display.flip()
    #         pygame.time.wait(60)
    #
    # print("Status: Finished Outputting Slices")
    # pygame.quit()

