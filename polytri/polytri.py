#!/usr/bin/env python

#stdlib imports
import ctypes
import sys
import os.path
import math

class PolyTriException(Exception):
    '''Used for exceptions with getTriangles'''

def isTriangle(p1,p2,p3,p4,p5,p6):
    if p2 == p3 and p4 == p5 and p6 == p1:
        return True
    if p1 == p3 and p4 == p5 and p6 == p2:
        return True
    if p1 == p4 and p3 == p5 and p6 == p2:
        return True
    if p1 == p4 and p3 == p6 and p5 == p2:
        return True
    if p2 == p4 and p3 == p5 and p6 == p1:
        return True
    if p2 == p4 and p3 == p6 and p5 == p1:
        return True
    if p2 == p3 and p4 == p6 and p5 == p1:
        return True
    return False

def getMissingTriangle(x1,y1,x2,y2,triangles):
    segments = []
    for triangle in triangles:
        xv,yv = triangle
        if (x1 in xv and y1 in yv) or (x2 in xv and y2 in yv):
            segments.append((xv[0],yv[0],xv[1],yv[1]))
            segments.append((xv[0],yv[0],xv[2],yv[2]))
            segments.append((xv[1],yv[1],xv[2],yv[2]))
    for i in range(0,len(segments)):
        bsegment = segments[i]
        for j in range(1,len(segments)):
            if i == j:
                continue
            csegment = segments[j]
            p1 = (x1,y1)
            p2 = (x2,y2)
            p3 = (bsegment[0],bsegment[1])
            p4 = (bsegment[2],bsegment[3])
            p5 = (csegment[0],csegment[1])
            p6 = (csegment[2],csegment[3])
            if isTriangle(p1,p2,p3,p4,p5,p6):
                xv = []
                yv = []
                triangle = []
                points = [p1,p2,p3,p4,p5,p6]
                for point in points:
                    if point not in triangle:
                        triangle.append(point)
                        xv.append(point[0])
                        yv.append(point[1])
                triangle = (xv,yv)
                return triangle
    return None

def floatify(triangles,precision):
    newtriangles = []
    for triangle in triangles:
        xv,yv = triangle
        xv = [float(xi)/math.pow(10,precision) for xi in xv]
        yv = [float(yi)/math.pow(10,precision) for yi in yv]
        newtriangles.append((xv,yv))
    return newtriangles
    
def getTriangles(xpoly,ypoly,precision=4):
    '''Partition a polygon (convex or concave, but without any holes) into a set of triangles.  
    Floating point polygons will be converted to integers with precision digits, triangularized, 
    then converted back to floats.  For example, the polygon:
    xpoly=(1.123,2.456,3.789,4.123)
    ypoly=(1.123,2.456,3.789,4.123)
    would be converted to:

    xpoly=(11230,24560,37890,41230)
    ypoly=(11230,24560,37890,41230)

    triangularized, then the vertices converted back to floats using the same precision.
    
    @param xpoly: Sequence of x coordinates (int or float)
    @param ypoly: Sequence of y coordinates (int or float)
    @keyword precision: Floating point values will be multiplied by 10^precision, rounded, and converted to ints.
    @return: A list of triangles, where each triangle is defined as two tuples containing x vertices and y vertices.
    '''
    foundfile = False
    for p in sys.path:
        trifile = os.path.join(p,'tri.so')
        if os.path.isfile(trifile):
            foundfile = True
            break
    if not foundfile:
        raise PolyTriException('Cannot find shared object file tri.so')

    if len(xpoly) != len(ypoly):
        raise PolyTriException('Input xpoly and ypoly not the same length')
    
    #check to see if any elements in xpoly or ypoly are floats - if so, treat them all as floats
    #since this C library only handles integers, convert floats to ints by multiplying them 
    #by 10^precision and then dividing by that when we're all done.
    xfloat = sum([isinstance(x,float) for x in xpoly])
    yfloat = sum([isinstance(y,float) for y in ypoly])
    isFloat = False
    if xfloat or yfloat:
        isFloat = True
        xpoly = [int(round(x*math.pow(10,precision))) for x in xpoly]
        ypoly = [int(round(y*math.pow(10,precision))) for y in ypoly]

    #since we don't know how many triangles we will have, but we can't have any more
    #than we have vertices, and we're dealing with C code which isn't very good at creating dynamically
    #sized arrays, we'll tell it to expect nvertices number of triangles output.
    #initialize our output arrays with a hopefully unlikely integer, so that we can flag those unfilled
    #array indices later
    missing = -99999
    nvertices = len(xpoly)
    trilib = ctypes.cdll.LoadLibrary(trifile)
    IntList = ctypes.c_int * nvertices
    x = IntList(*xpoly)
    y = IntList(*ypoly)

    #C function definition is: 
    #void LoadVertices(int x[],int y[],int npoints);
    trilib.LoadVertices(x,y,nvertices)

    #create 6 arrays of input x and y values to be filled in by triangulate routine
    xverts1 = IntList(*[missing]*nvertices)
    yverts1 = IntList(*[missing]*nvertices)
    xverts2 = IntList(*[missing]*nvertices)
    yverts2 = IntList(*[missing]*nvertices)
    xverts3 = IntList(*[missing]*nvertices)
    yverts3 = IntList(*[missing]*nvertices)

    #C function definition is: 
    #void	Triangulate(int xtri1[], int ytri1[], int xtri2[], int ytri2[], int xtri3[], int ytri3[]);
    trilib.Triangulate(xverts1,yverts1,xverts2,yverts2,xverts3,yverts3)
    
    #convert C int arrays to lists
    xv1 = list(xverts1)
    yv1 = list(yverts1)
    xv2 = list(xverts2)
    yv2 = list(yverts2)
    xv3 = list(xverts3)
    yv3 = list(yverts3)

    #delete all of our malloc-ed variables
    del x,y,xverts1,yverts1,xverts2,yverts2,xverts3,yverts3
    trilib.dlclose(trilib._handle) #close the library
    del trilib #delete the library, just in case there are some pointers floating around
    
    #remove missing data values
    xv1[:] = [xvi for xvi in xv1 if xvi != missing]
    yv1[:] = [yvi for yvi in yv1 if yvi != missing]

    xv2[:] = [xvi for xvi in xv2 if xvi != missing]
    yv2[:] = [yvi for yvi in yv2 if yvi != missing]

    xv3[:] = [xvi for xvi in xv3 if xvi != missing]
    yv3[:] = [yvi for yvi in yv3 if yvi != missing]

    #smoosh these arrays into the output data structure we desire
    #list of ((x1,x2,x3),(y1,y2,y3)) triangles.
    triangles = []
    triangle_indices = []
    for i in range(0,len(xv1)):
        triangle = ((xv1[i],xv2[i],xv3[i]),(yv1[i],yv2[i],yv3[i]))
        i1 = xpoly.index(xv1[i])
        i2 = xpoly.index(xv2[i])
        i3 = xpoly.index(xv3[i])
        indices = [i1,i2,i3]
        indices.sort()
        triangle_idx = (indices)
        triangles.append(triangle)
        triangle_indices.append(triangle_idx)

    #check to see if all polygon line segments are a part of a triangle
    missing_segments = []
    for i1 in range(0,len(xpoly)-1):
        i2 = i1+1
        found = 0
        for triangle_idx in triangle_indices:
            if i1 in triangle_idx and i2 in triangle_idx:
                found += 1
        if found == 0:
            if i not in missing_segments:
                missing_segments.append(i)

    #now check every 
    for iseg in missing_segments:
        x1 = xpoly[iseg]
        y1 = ypoly[iseg]
        x2 = xpoly[iseg+1]
        y2 = ypoly[iseg+1]
        triangle = getMissingTriangle(x1,y1,x2,y2,triangles)
        triangles.append(triangle)

    if isFloat:
        triangles = floatify(triangles,precision)
        
    return triangles
    
def main():
    #example from Computational Geometry in C book
    xpoly = [0,10,12,20,13,10,12,14,8,6,10,7,0,1,3,5,-2,5]
    ypoly = [0,7,3,8,17,12,14,9,10,14,15,18,16,13,15,8,9,5]
    triangles = getTriangles(xpoly,ypoly)
    for triangle in triangles:
        print triangle

    #let's do some floating point values
    xpoly = [-119.0+(xp/10.0) for xp in xpoly]
    ypoly = [32.0+(yp/10.0) for yp in ypoly]
    triangles = getTriangles(xpoly,ypoly)
    for triangle in triangles:
        print triangle
if __name__ == '__main__':
    main()
