from distutils.core import setup,Extension

module1 = Extension('tri',
                    sources = ['polytri/tri.c'])

setup(name='polytri',
      version='0.1dev',
      description='Partition polygon into triangles',
      author='Mike Hearne',
      author_email='mhearne@usgs.gov',
      url='',
      packages=['polytri'],
      scripts = [],
      ext_modules = [module1],
)
