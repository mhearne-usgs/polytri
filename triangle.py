#!/usr/bin/env python

#stdlib imports
import argparse
import sys

#local imports
from polytri.polytri import getTriangles

def writeTriangles(xpoly,ypoly,outfile,precision):
    xint = sum([xp-int(xp) == 0 for xp in xpoly])
    yint = sum([yp-int(yp) == 0 for yp in ypoly])

    #check to see if all vertices are actually integers
    fmt = '%f %f %f %f %f %f\n'
    if xint == len(xpoly) and yint == len(ypoly):
        xpoly = [int(xp) for xp in xpoly]
        ypoly = [int(yp) for yp in ypoly]
        fmt = '%i %i %i %i %i %i\n'
    
    triangles = getTriangles(xpoly,ypoly,precision=precision)
    for triangle in triangles:
        xv,yv = triangle
        tupleout = tuple(xv + yv)
        outfile.write(fmt % tupleout)

def main(args):
    if args.infile is None:
        xylines = sys.stdin.readlines()
    else:
        xylines = open(args.infile,'rt').readlines()

    xpoly = []
    ypoly = []
    if args.outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(args.outfile,'wt')
    for line in xylines:
        if line.strip().startswith('#'):
            writeTriangles(xpoly,ypoly,outfile,args.precision)
            
        xt,yt = line.split()
        x = float(xt)
        y = float(yt)
        xpoly.append(x)
        ypoly.append(y)
        
    writeTriangles(xpoly,ypoly,outfile,args.precision)

    if args.outfile is not None:
        outfile.close()

if __name__ == '__main__':
    desc = '''Partition polygon into triangles.
    Input polygons can be concave or convex, but must not contain any holes.
    Input format:
    x1 y1
    x2 y2
    x3 y3
    ...
    xN yN

    Multi-part polygons can be input by separating the polygons with lines starting with #.
    x1 y1
    x2 y2
    x3 y3
    #
    x1 y1
    x2 y2
    x3 y3

    Polygon vertices can be integer or floating point values.


    Output format:
    x1 x2 x3 y1 y2 y3 #one triangle
    x1 x2 x3 y1 y2 y3 #second triangle
    ...
    
    
    Usage:
    When used with no positional arguments, the program assumes that x,y pairs will arrive
    via stdin, and output will be printed to stdout.
    When used with one positional argument, that argument will be presumed to be an input text file,
    and output will be printed to stdout.
    When used with two positional argument, they are presumed to be the input and output file names.
    '''
    prechelp = '''Set precision of float->int conversion. 
    If dealing with lat/lon values, here is a helpful guide:
    6 digits of precision is approximately 10 cm.
    5 digits of precision is approximately 1 meter.
    4 digits of precision (the default) is approximately 10 meters.
    '''
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', nargs='?',
                        help='Input file')
    parser.add_argument('outfile', nargs='?',
                        help='Output file')
    parser.add_argument('-p', dest='precision', type=int, default=4,
                        help=prechelp)

    arguments = parser.parse_args()
    main(arguments)
