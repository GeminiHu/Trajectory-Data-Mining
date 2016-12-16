from distutils.core import setup
from Cython.Build import cythonize
setup(name = 'CEasyMatching',
      ext_modules = cythonize("haversine.pyx"))