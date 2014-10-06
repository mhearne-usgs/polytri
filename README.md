polytri
=======

polytri is a library which provides the functionality to extract all
unique triangle vertices from a convex or concave polygon (without holes!).  

The library is (for now) based on the code found at this Google Code page:
https://code.google.com/p/poly2tri/source/browse/python/seidel.py?repo=archive&r=96caf237ea676601374ae9d492fe4feb8514b695

The seidel module is included here for ease of installation.

Initial versions of this package used a modified version of Joseph O'Rourke's C triangulate 
routines, found here:

http://cs.smith.edu/~orourke/CGCode/SecondEdition/Ccode2.tar.gz

From his excellent book, "Computational Geometry in C":

http://cs.smith.edu/~orourke/books/compgeom.html

The modified C code is gratefully included with the permission of the original author.

However, these modifications failed with further testing.  The seidel
module above seemed to work well for all use cases tested by the
author.  As time permits, the O'Rourke wrapper will be tested and
hopefully re-incorporated back into this package.

Installation and Dependencies
=============================

This package *should* be completely self-contained if your Python vintage is 2.5 or greater.

This installation does not *currently* require that you have a C compiler
installed, but it may again in the future (see note above).

To install:
pip install git+git://github.com/mhearne-usgs/polytri.git

Usage
======

This repository contains one script which allows you to convert polygons into triangles from the command line:
<pre>
usage: triangle.py [-h] [-p PRECISION] [infile] [outfile]

Partition polygon into triangles.
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
    

positional arguments:
  infile        Input file
  outfile       Output file

optional arguments:
  -h, --help    show this help message and exit
  -p PRECISION  Set precision of float->int conversion. If dealing with
                lat/lon values, here is a helpful guide: 6 digits of precision
                is approximately 10 cm. 5 digits of precision is approximately
                1 meter. 4 digits of precision (the default) is approximately
                10 meters.

</pre>

Usage as a Python library:

<pre>
from polytri.polytri import getTriangles

xpoly = [0,10,12,20,13,10,12,14,8,6,10,7,0,1,3,5,-2,5]
ypoly = [0,7,3,8,17,12,14,9,10,14,15,18,16,13,15,8,9,5]
triangles = getTriangles(xpoly,ypoly)
for triangle in triangles:
    print triangle
</pre>

The only currently interesting function is getTriangles(), which takes in X and Y
sequences and returns a list of triangles, where each triangle is defined as two 
tuples containing three x and y vertices.

An IPython notebook demonstrating the usage (with plots) is included in this repository.  Note that 
while this library can be used with most "stock" Python distributions, the notebook requires IPython and 
matplotlib. 

<a href="http://nbviewer.ipython.org/github/mhearne-usgs/polytri/blob/master/notebooks/polytri_examples.ipynb">polytri notebook</a>

