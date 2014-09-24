polytri
=======

polytri is a library which provides the functionality to extract all
unique triangle vertices from a convex or concave polygon.  The library is
a fairly thin ctypes (https://docs.python.org/2.7/library/ctypes.html#module-ctypes)
wrapper around a modified version of Joseph O'Rourke's C triangulate routines, found here:

http://cs.smith.edu/~orourke/CGCode/SecondEdition/Ccode2.tar.gz

From his excellent book, <u>Computational Geometry in C</u>:

http://cs.smith.edu/~orourke/books/compgeom.html

The modified C code is gratefully included with the permission of the original author.

Installation and Dependencies
=============================

This package *should* be completely self-contained if your Python vintage is 2.5 or greater.
It does contain some C code (see note above), which will require that you have a C compiler
installed and configured to work with Python.

Usage
======

A command line script to convert polygons into triangles is planned but not yet implemented.
Currently the usage is as a Python library:

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

http://nbviewer.ipython.org/github/mhearne-usgs/polytri/blob/master/notebooks/polytri_examples.ipynb

TODO
====

* As mentioned above, write a command line script for non-Pythonistas.
* Figure out why the notebook crashes when getTriangles() is called multiple times (not reproducible in console or script).

